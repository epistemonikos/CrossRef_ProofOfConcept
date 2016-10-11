import requests
from flask import render_template, make_response, json, abort, jsonify
from flask_restful import Resource, reqparse
from werkzeug.utils import redirect

from reflookup import app, api
from urllib.parse import unquote

from rating.rating import Rating

from reflookup.search_form import CrossRefForm
from reflookup.ris_utils.convert import dict2ris, RISTypeException

"""
This file contains the endpoint resources for looking up references in
CrossRef.
"""

from standardJson import crossref_to_standard


def cr_citation_lookup(citation):
    """
    This function does the actual CrossRef API call to search for a given
    citation, and returns the first (and thus, according to CR, the best)
    result.
    :param citation: Citation to look up in CR.
    :return: A Python dict representing the best result offered by CrossRef.
    """
    params = {'query': citation}
    url = app.config['CROSSREF_URI']

    req = requests.get(url, params=params)
    if req.status_code != 200:
        abort(req.status_code, 'Remote API error.')

    rv = req.json()

    if len(rv['message']['items']) < 1:
        abort(404, 'No results found for query.')

    result = rv['message']['items'][0]
    result = crossref_to_standard(result)
    result['rating'] = Rating(citation, result).value()

    return result


# TODO: FIX
@api.representation('application/x-research-info-systems')
def serve_ris(data, code, headers=None):
    """
    Helper function to parse a CrossRef return JSON into a valid RIS.
    Deprecated. TODO: Replace with general-purpose parsing function.
    :param data: Data to pack in a flask response.
    :param code: HTTP status code of the response.
    :param headers: Headers of the response.
    :return: A packed response containing the parsed RIS document, or,
    if it fails, the original JSON data.
    """
    try:
        ris_data = dict2ris(data)
        resp = make_response(ris_data, code)
    except RISTypeException:
        resp = make_response(json.dumps(data), 501)

    resp.headers.extend(headers or {})
    return resp


class CrossRefLookupResource(Resource):
    """
    This resource represents the /crsearch endpoint on the API.
    """

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
    """
    This resource represents the / endpoint, and its associated form.
    """

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

        json = cr_citation_lookup(query.strip())
        return json
