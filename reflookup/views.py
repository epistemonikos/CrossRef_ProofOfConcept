from reflookup import api, app
from reflookup.crossref_lookup.views import CrossRefLookupResource, CrossRefSearchForm

prefix = app.config['API_PREFIX']
api.add_resource(CrossRefLookupResource, prefix + '/crsearch')
api.add_resource(CrossRefSearchForm, "/")
