import requests
from flask import render_template, make_response, json, abort
from flask_restful import Resource, reqparse
from werkzeug.utils import redirect

from reflookup import app, api
from urllib.parse import unquote

from rating.rating import Rating

from reflookup.search_form import CrossRefForm
from reflookup.ris_utils.convert import dict2ris, RISTypeException


def cr_citation_lookup(citation):
    params = {'query': citation}
    url = app.config['CROSSREF_URI']

    req = requests.get(url, params=params)
    if req.status_code != 200:
        abort(req.status_code, "Remote service returned an unexpected HTTP "
                               "status code.")

    rv = req.json()

    if len(rv['message']['items']) < 1:
        abort(404, 'No results found for query "{q}".'.format(q=citation))

    result = rv['message']['items'][0]
    result['rating'] = Rating(citation, result).value()

    return result


@api.representation('application/x-research-info-systems')
def serve_ris(data, code, headers=None):
    try:
        ris_data = dict2ris(data)
        resp = make_response(ris_data, code)
    except RISTypeException:
        resp = make_response(json.dumps(data), 501)

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
