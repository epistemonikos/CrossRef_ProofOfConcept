import threading
from email.utils import unquote

from flask import make_response, render_template
from werkzeug.utils import redirect

from rating.chooser import Chooser
from reflookup.crossref_lookup.views import cr_citation_lookup
from reflookup.mendeley_lookup.views import mendeley_lookup
from flask_restful import Resource
from flask_restful.reqparse import RequestParser

from reflookup.search_form import ReferenceLookupForm


def lookup_crossref(ref, ret):
    ret['result'] = cr_citation_lookup(ref)


def lookup_mendeley(ref, ret):
    ret['result'] = mendeley_lookup(ref)


def integrated_lookup(citation):
    # create threads to get results from Mendeley and Crossref at the
    # same time

    cr = {}
    md = {}

    t1 = threading.Thread(target=lookup_crossref, args=(citation, cr))
    t2 = threading.Thread(target=lookup_mendeley, args=(citation, md))

    t1.start()
    t2.start()

    t1.join()
    t2.join()

    chooser = Chooser(citation, [cr['result'], md['result']])

    return chooser.select()


class IntegratedLookupResource(Resource):
    def __init__(self):
        self.parser = RequestParser()
        self.parser.add_argument('ref', type=str, required=True,
                                 location='values')

    def get(self):
        data = self.parser.parse_args()
        ref = unquote(data['ref']).strip()

        return integrated_lookup(ref)

    def post(self):
        return self.get()


class SearchFormResource(Resource):
    """
    This resource represents the / endpoint, and its associated form.
    """

    def __init__(self):
        self.parser = RequestParser()
        self.parser.add_argument('query', location='form')

    def get(self):
        form = ReferenceLookupForm()
        if form.validate_on_submit():
            return redirect('/')

        res = make_response(render_template('form.html', form=form))
        return res

    def post(self):
        data = self.parser.parse_args()
        query = data.get('query', None)
        if not query:
            return self.get()

        json = integrated_lookup(query.strip())
        return json
