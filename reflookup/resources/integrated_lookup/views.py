import threading
from email.utils import unquote

from flask import make_response, render_template
from flask_restful import HTTPException
from flask_restful import Resource, abort
from flask_restful.reqparse import RequestParser
from werkzeug.utils import redirect

from reflookup.resources.lookup_functions.citation_search import \
    cr_citation_lookup, \
    mendeley_lookup
from reflookup.search_form import ReferenceLookupForm
from reflookup.utils.pubmed_id import getPubMedID
from reflookup.utils.rating.chooser import Chooser
from reflookup.utils.restful.utils import ExtResource, DeferredResource
from reflookup.utils.standardize_json import StandardDict


def lookup_crossref(ref, ret, return_all=False):
    """
  Crossref lookup wrapper, used for threading
  :param ref: Citation for lookup in Crossref
  :param ret: Aux variable for result submitting
  :param return_all: Optional parameter indicating to return whole list of results instead of only the first.
  """
    try:
        ret['result'] = cr_citation_lookup(ref, return_all)
    except HTTPException as e:
        ret['result'] = None
        ret['code'] = e.code
        ret['description'] = e.description


def lookup_mendeley(ref, ret, return_all=False):
    """
  Mendeley lookup wrapper, used for threading
  :param ref: Citation for lookup in Mendeley
  :param ret: Aux variable for result submitting
  :param return_all: Optional parameter indicating to return whole list of results instead of only the first.
  """
    try:
        ret['result'] = mendeley_lookup(ref, return_all)
    except HTTPException as e:
        ret['result'] = None
        ret['code'] = e.code
        ret['description'] = e.description


def integrated_lookup(citation, return_all=False, return_both=False):
    """
    Mendeley & Crossref integrated lookup. By default this function returns the highest ranked
    result, but can be moified to return the whole list or the best result of each service
    :param citation: Given citation for lookup
    :param return_all: Optional parameter indicating to return whole list of results instead of only the first.
    :param return_both: Optional parameter indicating to return the best results of each serrvice.
    :return: Respective citation lookup result
    """
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

    if not cr.get('result', None) and not md.get('result', None):
        if cr.get('code', None) == 404:
            abort(404,
                  message='No results found for query {}'.format(citation))
        elif cr.get('code', None) == md.get('code', None):
            abort(cr.get('code'), message=cr.get('description'))
        else:
            abort(500, message='Remote services returned with error codes.'
                               'Crossref: {crcode} - {crdesc}'
                               'Mendeley: {mdcode} - {mddesc}'.format(
                crcode=cr.get('code'), crdesc=cr.get('description'),
                mdcode=md.get('code'), mddesc=md.get('description')))

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
    """
    Mendeley & Crossref integrated lookup. This one receives a list of references and resolves them based on the
    integrated lookup, returning only the best result of each citation with it's respective pubmedI lookpu result
    :param refl: List of references to resolve
    :return: List of reference lookup results
    """
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

        result = integrated_lookup(query.strip(), return_all=get_all)

        ret_dict = {
            'length': 0,
            'result': []
        }

        if get_all:
            for r in result:
                ret_dict['result'].append(getPubMedID(r))
            ret_dict['length'] = len(ret_dict['result'])
        else:
            ret_dict['result'].append(getPubMedID(result))
            ret_dict['length'] = 1

        return ret_dict


class BatchLookupResource(DeferredResource):
    """
    Endpoint for batch lookups.
    POST -> Receives a json containing a list of references to check,
    returns a job ID to check on.
    GET -> Receives a job ID and returns the completion status and results.
    """

    def __init__(self):
        super().__init__()
        self.post_parser.add_argument('refs', type=list, location='json',
                                      required=True)
        self.post_parser.add_argument('length', type=int, location='json',
                                      required=True)

    def post(self):
        params = self.post_parser.parse_args()
        refs = params['refs']
        if params['length'] != len(refs):
            abort(400)

        return self.enqueue_job_and_return(batch_lookup, refs)
