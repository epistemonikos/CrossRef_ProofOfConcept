from urllib.parse import unquote

from flask_restful import reqparse

from reflookup.resources.lookup_functions.citation_extract import get_scopus_references
from reflookup.utils.restful.utils import ExtResource

"""
This file contains the endpoint resources for retrieving references from Scopus
"""


class ScopusReferenceExtractResource(ExtResource):
    """
        This resource represents the /refs/scopus endpoint on the API.
    """

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('doi', type=str, required=True,
                                 location='values')

    def get(self):
        data = self.parser.parse_args()
        doi = unquote(data['doi']).strip()
        return get_scopus_references(doi)

    def post(self):
        return self.get()
