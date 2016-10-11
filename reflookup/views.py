from reflookup import api, app
from reflookup.crossref_lookup.views import CrossRefLookupResource
from reflookup.mendeley_lookup.views import MendeleyLookupResource
from reflookup.integrated_lookup.views import IntegratedLookupResource, \
    SearchFormResource

prefix = app.config['API_PREFIX']
api.add_resource(CrossRefLookupResource, prefix + '/crsearch')
api.add_resource(SearchFormResource, "/")
api.add_resource(MendeleyLookupResource, prefix + '/mdsearch')
api.add_resource(IntegratedLookupResource, prefix + '/search')
