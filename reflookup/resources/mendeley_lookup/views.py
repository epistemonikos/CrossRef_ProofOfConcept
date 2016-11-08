from urllib.parse import unquote

from flask_restful import reqparse

from reflookup.resources.lookup_functions.citation_search import mendeley_lookup
from reflookup.utils.restful.utils import ExtResource

"""
This file contains the endpoint resources for looking up references in
Mendeley.
"""


class MendeleyLookupResource(ExtResource):
    """
        This resource represents the /mdsearch endpoint on the API.
        """

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('ref', type=str, required=True,
                                 location='values')

    def get(self):
        data = self.parser.parse_args()
        ref = unquote(data['ref']).strip()
        return mendeley_lookup(ref)

    def post(self):
        return self.get()


