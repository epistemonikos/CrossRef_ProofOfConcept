from reflookup.utils.restful.utils import DeferredResource
from reflookup.utils.pubmed_id import getPubMedID
from reflookup.resources.search_v2.functions import single_search
from reflookup.resources.extract_v2.functions import extract_refs


def lookup_and_extract(citation):
    ref = getPubMedID(single_search(citation))

    doi = ref.get('ids', {}).get('doi', None)
    pmid = ref.get('ids', {}).get('pubmed', None)
    url = ref.get('ids', {}).get('scopus', None)

    dois = [doi] if doi else []
    pmids = [pmid] if pmid else []
    urls = [url] if url else []

    extracted_refs = extract_refs(dois, urls, pmids)
    ref['refs'] = extracted_refs

    return ref


class IntegratedSearchAndExtractV2(DeferredResource):
    def __init__(self):
        super().__init__()
        self.get_parser.add_argument('q', required=True, type=str)

    def get(self):
        args = self.get_parser.parse_args()
        return self.enqueue_job_and_return(lookup_and_extract, args['q'])
