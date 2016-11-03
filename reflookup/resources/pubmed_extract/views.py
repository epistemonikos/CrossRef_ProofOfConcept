from urllib.parse import unquote

from reflookup.resources.lookup_functions.citation_extract import getRefID, \
    getReferenceInfo
from reflookup.utils.restful.utils import DeferredResource


def deferred_extract_references(pmid):
    return getReferenceInfo(getRefID(pmid))


class PubmedReferenceExtractResource(DeferredResource):
    """
        This resource represents the /refs/pubmed endpoint on the API.
    """

    def __init__(self):
        super().__init__()
        self.post_parser.add_argument('pmid', type=str, required=True,
                                      location='values')

    def post(self):
        data = self.post_parser.parse_args()
        pmid = unquote(data['pmid']).strip()

        return self.enqueue_task_and_return(deferred_extract_references, pmid)
