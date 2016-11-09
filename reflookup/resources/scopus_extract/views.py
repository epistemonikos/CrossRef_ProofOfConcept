from urllib.parse import unquote

from reflookup.resources.lookup_functions.citation_extract import \
    get_scopus_references
from reflookup.utils.restful.utils import DeferredResource
from reflookup.utils.pubmed_id import getPubMedID

"""
This file contains the endpoint resources for retrieving references from Scopus
"""


def deferred_extract_references(doi):
    res = get_scopus_references(doi)
    results = []
    for r in res:
        results.append(getPubMedID(r))
    return results


class ScopusReferenceExtractResource(DeferredResource):
    """
        This resource represents the /refs/scopus endpoint on the API.
    """

    def __init__(self):
        super().__init__()
        self.post_parser.add_argument('doi', type=str, required=True,
                                      location='values')

    def post(self):
        data = self.post_parser.parse_args()
        doi = unquote(data['doi']).strip()

        return self.enqueue_job_and_return(deferred_extract_references, doi)
