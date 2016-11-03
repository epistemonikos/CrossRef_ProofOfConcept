from quick_references import api, app
from quick_references.resources.scopus.views import ScopusResource

prefix = app.config['API_PREFIX']
api.add_resource(ScopusResource, prefix + '/refs/scopus')
