import threading
from datetime import datetime, timezone
from email.utils import unquote

import redis
from flask import make_response, render_template
from flask_restful import Resource, abort
from flask_restful.reqparse import RequestParser
from werkzeug.utils import redirect

from reflookup.resources.lookup_functions import cr_citation_lookup, \
    mendeley_lookup
from reflookup.search_form import ReferenceLookupForm
from reflookup.utils.pubmed_id import getPubMedID
from reflookup.utils.rating.chooser import Chooser
from reflookup.utils.restful.utils import ExtResource, EncodingResource
from reflookup.utils.standardize_json import StandardDict
from itsdangerous import URLSafeSerializer, BadSignature
from reflookup import app, rq

taskserializer = URLSafeSerializer(app.secret_key, salt='task')


def lookup_crossref(ref, ret, return_all=False):
    ret['result'] = cr_citation_lookup(ref, return_all)


def lookup_mendeley(ref, ret, return_all=False):
    ret['result'] = mendeley_lookup(ref, return_all)


def integrated_lookup(citation, return_all=False, return_both=False):
    # create threads to get results from Mendeley and Crossref at the
    # same time

    cr = {}
    md = {}

    t1 = threading.Thread(target=lookup_crossref,
                          args=(citation, cr, return_all))
    t2 = threading.Thread(target=lookup_mendeley,
                          args=(citation, md, return_all))

    t1.start()
    t2.start()

    t1.join()
    t2.join()

    if return_all:
        def get_rating(result):
            return result.get('rating', {}).get('total', 0)

        results = cr.get('result', []) + md.get('result', [])
        results = sorted(results, key=get_rating)
        results.reverse()
        return results

    elif return_both:
        results = []
        if md.get('result', None):
            results.append(md.get('result'))
        if cr.get('result', None):
            results.append(cr.get('result'))

        return results

    else:
        chooser = Chooser(citation, [cr.get('result',
                                            StandardDict().getEmpty()),
                                     md.get('result',
                                            StandardDict().getEmpty())])

        return chooser.select()


def batch_lookup(refl):
    results = []

    for ref in refl:
        res = integrated_lookup(ref, return_all=False)
        res = getPubMedID(res)
        results.append(res)

    return results


class IntegratedLookupResource(ExtResource):
    """
    Endpoint in charge of doing the integrated lookup between Mendeley and
    Crossref
    """

    def __init__(self):
        self.parser = RequestParser()
        self.parser.add_argument('ref', type=str, required=True,
                                 location='values')
        self.parser.add_argument('getall', type=bool, required=False,
                                 location='values')
        self.parser.add_argument('getboth', type=bool, required=False,
                                 location='values')

    def get(self):
        data = self.parser.parse_args()
        ref = unquote(data['ref']).strip()
        get_all = data.get('getall', False)
        get_both = data.get('getboth', False)

        return integrated_lookup(ref, return_all=get_all, return_both=get_both)

    def post(self):
        return self.get()


class SearchFormResource(Resource):
    """
    This resource represents the / endpoint, and its associated form.
    """

    def __init__(self):
        self.parser = RequestParser()
        self.parser.add_argument('query', location='form')
        self.parser.add_argument('chkbox', type=bool, location='form')

    def get(self):
        form = ReferenceLookupForm()
        if form.validate_on_submit():
            return redirect('/')

        res = make_response(render_template('form.html', form=form))
        return res

    def post(self):
        data = self.parser.parse_args()
        query = data.get('query', None)
        get_all = data.get('chkbox', False)
        if not query:
            return self.get()

        json = integrated_lookup(query.strip(), return_all=get_all)

        ret_dict = {
            'length': 0,
            'result': []
        }

        if get_all:
            for r in json.get('results', []):
                ret_dict['result'].append(getPubMedID(r))
            ret_dict['length'] = len(ret_dict['result'])
        else:
            ret_dict['result'].append(getPubMedID(json))
            ret_dict['length'] = 1

        return ret_dict


class BatchLookupResource(EncodingResource):
    """
    Endpoint for batch lookups.
    POST -> Receives a json containing a list of references to check,
    returns a job ID to check on.
    GET -> Receives a job ID and returns the completion status and results.
    """

    def __init__(self):
        self.post_parser = RequestParser()
        self.post_parser.add_argument('refs', type=list, location='json',
                                      required=True)
        self.post_parser.add_argument('length', type=int, location='json',
                                      required=True)

        self.get_parser = RequestParser()
        self.get_parser.add_argument('id', type=str, location='values',
                                     required=True)

        self.result_ttl = app.config['RESULT_TTL_SECONDS']

    def post(self):
        params = self.post_parser.parse_args()
        refs = params['refs']
        if params['length'] != len(refs):
            abort(400)

        try:
            job = rq.enqueue(batch_lookup, refs, result_ttl=self.result_ttl)
            job_id = taskserializer.dumps(job.id)
        except redis.exceptions.ConnectionError:
            abort(500)

        return {
                   'job': job_id,
                   'submitted': datetime.now(timezone.utc).isoformat()
               }, 202

    def get(self):
        job_id = self.get_parser.parse_args()['id']
        try:
            job_id = taskserializer.loads(job_id)
        except BadSignature:
            abort(400, message='Invalid job id')

        job = rq.fetch_job(job_id)
        if not job:
            abort(400, message='Invalid job id')

        if not job.result:
            return {
                       'done': False,
                       'result': None,
                       'length': 0,
                       'result_ttl': self.result_ttl,
                       'timestamp': None
                   }, 202
        else:
            return {
                       'done': True,
                       'result': job.result,
                       'length': len(job.result),
                       'result_ttl': self.result_ttl,
                       'timestamp': job.ended_at.isoformat()
                   }, 200
