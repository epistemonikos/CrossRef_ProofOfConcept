from quick_references import api, app
from reflookup.resources.scopus import ScopusResource

prefix = app.config['API_PREFIX']
api.add_resource(ScopusResource, prefix + '/refs/scopus')
