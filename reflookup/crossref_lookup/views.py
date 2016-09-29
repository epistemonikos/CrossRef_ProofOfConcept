import requests
from flask import render_template, make_response
from flask_restful import Resource, reqparse
from werkzeug.utils import redirect

from reflookup import app, api
from urllib.parse import unquote

from reflookup.search_form import CrossRefForm
from reflookup.ris_utils.convert import dict2ris


def cr_citation_lookup(citation):
    params = {'query': citation}
    url = app.config['CROSSREF_URI']

    rv = requests.get(url, params=params).json()
    result = rv['message']['items'][0]

    return result


@api.representation('application/x-research-info-systems')
def serve_ris(data, code, headers=None):
    ris_data = dict2ris(data)
    resp = make_response(ris_data, code)
    resp.headers.extend(headers or {})
    return resp


class CrossRefLookupResource(Resource):
    def __init__(self):
        self.post_parser = reqparse.RequestParser()
        self.post_parser.add_argument('ref', type=str, required=True,
                                      location='values')

    def post(self):
        data = self.post_parser.parse_args()
        ref = unquote(data['ref']).strip()

        return cr_citation_lookup(ref)

    def get(self):
        return self.post()


class CrossRefSearchForm(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('query', location='form')

    def get(self):
        form = CrossRefForm()
        if form.validate_on_submit():
            return redirect('/')

        res = make_response(render_template('form.html', form=form))
        return res

    def post(self):
        data = self.parser.parse_args()
        query = data.get('query', None)
        if not query:
            return self.get()

        url = cr_citation_lookup(query.strip())['URL']
        return redirect(url)
