from reflookup import api, app
from reflookup.crossref_lookup.views import CrossRefLookupResource

api_prefix = app.config['API_PREFIX']
api.add_resource(CrossRefLookupResource, api_prefix + '/crsearch')
