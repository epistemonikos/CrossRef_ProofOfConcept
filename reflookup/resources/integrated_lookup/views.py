import threading
from datetime import datetime, timezone
from email.utils import unquote

from flask import make_response, render_template
from flask_restful import Resource, abort
from flask_restful.reqparse import RequestParser
from werkzeug.utils import redirect

from reflookup.resources.lookup_functions import cr_citation_lookup, \
    mendeley_lookup
from reflookup.search_form import ReferenceLookupForm
from reflookup.utils.pubmed_id import getPubMedID
from reflookup.utils.rating.chooser import Chooser
from reflookup.utils.restful.utils import ExtResource
from reflookup.utils.standardize_json import StandardDict
from itsdangerous import URLSafeSerializer
from reflookup import app, rq

taskserializer = URLSafeSerializer(app.secret_key, salt='task')


def lookup_crossref(ref, ret, return_all=False):
    ret['result'] = cr_citation_lookup(ref, return_all)


def lookup_mendeley(ref, ret, return_all=False):
    ret['result'] = mendeley_lookup(ref, return_all)


def integrated_lookup(citation, return_all=False):
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

    if not return_all:
        chooser = Chooser(citation, [cr.get('result',
                                            StandardDict().getEmpty()),
                                     md.get('result',
                                            StandardDict().getEmpty())])

        return chooser.select()

    else:
        def get_rating(result):
            return result.get('rating', {}).get('total', 0)

        lcr = len(cr.get('result', []))
        lmd = len(md.get('result', []))

        results = cr.get('result', []) + md.get('result', [])
        results = sorted(results, key=get_rating)
        l = len(results)
        results.reverse()

        return {
            'list_result': True,
            'total': l,
            'crossref': lcr,
            'mendeley': lmd,
            'results': results
        }


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

    def get(self):
        data = self.parser.parse_args()
        ref = unquote(data['ref']).strip()
        get_all = data.get('getall', False)

        return integrated_lookup(ref, return_all=get_all)

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

        if get_all:
            nresults = []
            for r in json.get('results', []):
                nresults.append(getPubMedID(r))
            json['results'] = nresults
            return json
        else:
            return getPubMedID(json)


class BatchLookupResource(Resource):
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

        job = rq.enqueue(batch_lookup, refs, result_ttl=self.result_ttl)
        job_id = taskserializer.dumps(job.id)

        return {
                   'job': job_id,
                   'submitted': datetime.now(timezone.utc).isoformat()
               }, 202

    def get(self):
        job_id = self.get_parser.parse_args()['id']
        job_id = taskserializer.loads(job_id)

        job = rq.fetch_job(job_id)

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
