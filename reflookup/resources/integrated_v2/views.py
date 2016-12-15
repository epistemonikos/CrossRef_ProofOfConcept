from reflookup.auth.models import auth_required
from reflookup.utils.restful.utils import DeferredResource
from reflookup.utils.pubmed_id import getPubMedID
from reflookup.resources.search_v2.functions import single_search
from reflookup.resources.extract_v2.functions import extract_refs


def lookup_and_extract(citation_list):
    results = []

    for citation in citation_list:
        ref = getPubMedID(single_search(citation))

        doi = ref.get('ids', {}).get('doi', None)
        pmid = ref.get('ids', {}).get('pubmed', None)
        url = ref.get('ids', {}).get('scopus', None)

        dois = [doi] if doi else []
        pmids = [pmid] if pmid else []
        urls = [url] if url else []

        extracted_refs = extract_refs(dois, urls, pmids)
        ref['references'] = extracted_refs
        results.append(ref)

    return results


class IntegratedSearchAndExtractV2(DeferredResource):
    """
    A convenience endpoint to handle the complete workflow of this service.
    It takes a list of plaintext references, resolves them to JSON structures
    containing the relevant information and then it resolves its references.

    It works in a deferred fashion, so it returns a job id with which to check
    the results.
    """

    def __init__(self):
        super().__init__()
        self.get_parser.add_argument('q', required=True, type=str,
                                     action='append')

    @auth_required()
    def get(self):
        args = self.get_parser.parse_args()
        return self.enqueue_job_and_return(lookup_and_extract, args['q'])
