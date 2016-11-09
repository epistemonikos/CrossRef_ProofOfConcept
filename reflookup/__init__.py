import os

from flask import Flask
from flask_restful import Api
from itsdangerous import URLSafeSerializer
from redis import Redis
from rq import Queue

app = Flask(__name__)

# Quick References
app.config['SCOPUS_URI'] = 'https://api.elsevier.com/content/article/doi/'
app.config['SCOPUS_API_KEY'] = 'd1dd2bfada7ec327c3f4a3e316ec98b8'
app.config['SCOPUS_DTD'] = {
    "default": "http://www.elsevier.com/xml/svapi/article/dtd",
    "sb": "http://www.elsevier.com/xml/common/struct-bib/dtd",
    "ce": "http://www.elsevier.com/xml/common/dtd",
}

app.config['PDF_UPLOAD_FOLDER'] = 'uploads/pdf-extract/'

# RefLookup
app.config['CROSSREF_URI'] = 'http://api.crossref.org/works'
app.config['MENDELEY_SEARCH_URI'] = 'https://api.mendeley.com/search/catalog'
app.config['MENDELEY_CATALOG_URI'] = 'https://api.mendeley.com/catalog'
app.config['MENDELEY_AUTH_URI'] = 'https://api.mendeley.com/oauth/token'
app.config['MENDELEY_AUTH'] = ('3578', 'y43xcFyn1lNG7VT5')  # TODO: MOVE TO ENV

app.config['RESULT_TTL_SECONDS'] = 300
app.secret_key = os.environ.get('REFSERVICE_SECRETKEY', '12345')
app.config['API_PREFIX'] = '/api/v1'
api = Api(app)
conn = Redis()

# Redis queue:
rq = Queue(connection=conn)

taskserializer = URLSafeSerializer(app.secret_key, salt='task')

from reflookup.resources import views

if __name__ == '__main__':
    app.run(debug=True)
