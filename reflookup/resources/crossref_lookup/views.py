from urllib.parse import unquote

from flask_restful import reqparse

from reflookup.resources.lookup_functions.citation_search import cr_citation_lookup, \
    cr_doi_lookup
from reflookup.utils.restful.utils import ExtResource

"""
This file contains the endpoint resources for looking up references in
CrossRef.
"""


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


class CrossRefDoiLookupResource(ExtResource):
    """
    This resource represents the /crsearch endpoint on the API.
    """

    def __init__(self):
        self.post_parser = reqparse.RequestParser()
        self.post_parser.add_argument('doi', type=str, required=True,
                                      location='values')

    def post(self):
        data = self.post_parser.parse_args()
        doi = unquote(data['doi']).strip()

        return cr_doi_lookup(doi)

    def get(self):
        return self.post()
