from reflookup import api, app
from reflookup.resources.crossref_lookup.views import \
    CrossRefLookupResource, CrossRefDoiLookupResource
from reflookup.resources.integrated_lookup.views import \
    IntegratedLookupResource, SearchFormResource, BatchLookupResource
from reflookup.resources.mendeley_lookup.views import MendeleyLookupResource
from reflookup.resources.pdf_extract.views import PdfReferenceExtractResource
from reflookup.resources.scopus_extract.views import ScopusReferenceExtractResource
from reflookup.resources.pubmed_extract.views import PubmedReferenceExtractResource
from reflookup.resources.jobs.views import JobResource
from reflookup.resources.integrated_extract.views import IntegratedReferenceExtractResource
from reflookup.resources.parsers.views import ParserResource
from reflookup.resources.search_v2.views import IntegratedReferenceSearchV2

prefix_v1 = app.config['API_PREFIX_V1']
prefix_v2 = app.config['API_PREFIX_V2']
api.add_resource(CrossRefLookupResource, prefix_v1 + '/crsearch')
api.add_resource(CrossRefDoiLookupResource, prefix_v1 + '/crsearch/doi')
api.add_resource(SearchFormResource, '/')
api.add_resource(MendeleyLookupResource, prefix_v1 + '/mdsearch')
api.add_resource(IntegratedLookupResource, prefix_v1 + '/search')
api.add_resource(BatchLookupResource, prefix_v1 + '/search/batch')
api.add_resource(ScopusReferenceExtractResource, prefix_v1 + '/refs/scopus')
api.add_resource(PubmedReferenceExtractResource, prefix_v1 + '/refs/pubmed')
api.add_resource(PdfReferenceExtractResource, prefix_v1 + '/refs/pdf')
api.add_resource(JobResource, prefix_v1 + '/job')
api.add_resource(IntegratedReferenceExtractResource, prefix_v1 + '/refs')

api.add_resource(ParserResource, prefix_v1 + '/parse')

api.add_resource(IntegratedReferenceSearchV2, prefix_v2 + '/search')
