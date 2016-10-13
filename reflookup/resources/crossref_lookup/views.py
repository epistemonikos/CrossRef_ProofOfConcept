from urllib.parse import unquote

import requests
from flask import abort
from flask_restful import reqparse

from reflookup import app
from reflookup.utils.rating.rating import Rating
from reflookup.utils.restful.utils import ExtResource

"""
This file contains the endpoint resources for looking up references in
CrossRef.
"""

from reflookup.utils.standardize_json import crossref_to_standard


def cr_citation_lookup(citation, return_all=False):
    """
    This function does the actual CrossRef API call to search for a given
    citation, and returns the first (and thus, according to CR, the best)
    result.
    :param return_all: Optional parameter indicating to return whole list of results instead of only the first.
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

    if return_all:
        result = []
        for r in rv['message']['items']:
            std = crossref_to_standard(r)
            std['rating'] = Rating(citation, std).value()
            result.append(std)
        return result

    else:
        result = rv['message']['items'][0]
        result = crossref_to_standard(result)
        result['rating'] = Rating(citation, result).value()
        return result



# # TODO: FIX
# @api.representation('application/x-research-info-systems')
# def serve_ris(data, code, headers=None):
#     """
#     Helper function to parse a CrossRef return JSON into a valid RIS.
#     Deprecated. TODO: Replace with general-purpose parsing function.
#     :param data: Data to pack in a flask response.
#     :param code: HTTP status code of the response.
#     :param headers: Headers of the response.
#     :return: A packed response containing the parsed RIS document, or,
#     if it fails, the original JSON data.
#     """
#     try:
#         ris_data = dict2ris(data)
#         resp = make_response(ris_data, code)
#     except RISTypeException:
#         resp = make_response(json.dumps(data), 501)
#
#     resp.headers.extend(headers or {})
#     return resp


class CrossRefLookupResource(ExtResource):
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


