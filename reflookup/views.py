from reflookup import api, app
from reflookup.crossref_lookup.views import CrossRefLookupResource

prefix = app.config['API_PREFIX']
api.add_resource(CrossRefLookupResource, prefix + '/crsearch')
