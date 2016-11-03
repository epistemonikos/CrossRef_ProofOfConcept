from reflookup import api, app
from reflookup.resources.crossref_lookup.views import \
    CrossRefLookupResource, CrossRefDoiLookupResource
from reflookup.resources.integrated_lookup.views import \
    IntegratedLookupResource, SearchFormResource, BatchLookupResource
from reflookup.resources.mendeley_lookup.views import MendeleyLookupResource
from reflookup.resources.scopus_extract.views import ScopusResource

prefix = app.config['API_PREFIX']
api.add_resource(CrossRefLookupResource, prefix + '/crsearch')
api.add_resource(CrossRefDoiLookupResource, prefix + '/crsearch/doi')
api.add_resource(SearchFormResource, '/')
api.add_resource(MendeleyLookupResource, prefix + '/mdsearch')
api.add_resource(IntegratedLookupResource, prefix + '/search')
api.add_resource(BatchLookupResource, prefix + '/search/batch')
api.add_resource(ScopusResource, prefix + '/refs/scopus')
