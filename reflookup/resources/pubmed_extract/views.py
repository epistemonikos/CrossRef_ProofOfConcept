from urllib.parse import unquote

from flask_restful import reqparse
from reflookup.resources.lookup_functions.citation_extract import getRefID, \
    getReferenceInfo

from reflookup.utils.restful.utils import ExtResource


class PubmedReferenceExtractResource(ExtResource):
    """
        This resource represents the /refs/pubmed endpoint on the API.
    """

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('pmid', type=str, required=True,
                                 location='values')

    def get(self):
        data = self.parser.parse_args()
        pmid = unquote(data['pmid']).strip()

        return getReferenceInfo(getRefID(pmid))

    def post(self):
        return self.get()
