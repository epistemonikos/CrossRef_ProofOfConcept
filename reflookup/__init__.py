import os

from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from itsdangerous import URLSafeSerializer, URLSafeTimedSerializer
from redis import Redis
from rq import Queue
from sys import stderr
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/refservice.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
CORS(app, supports_credentials=True)

# SERVER
app.config['HOST'] = '0.0.0.0'
app.config['PORT'] = 5001

# Quick References
app.config['SCOPUS_URI'] = 'https://api.elsevier.com/content/article/doi/'
app.config['SCOPUS_API_KEY'] = os.environ.get('SCOPUS_API_KEY')
app.config['SCOPUS_DTD'] = {
    "default": "http://www.elsevier.com/xml/svapi/article/dtd",
    "sb": "http://www.elsevier.com/xml/common/struct-bib/dtd",
    "ce": "http://www.elsevier.com/xml/common/dtd",
    "prism": "http://prismstandard.org/namespaces/basic/2.0/",
    "dc": "http://purl.org/dc/elements/1.1/"
}

app.config['PDF_UPLOAD_FOLDER'] = 'uploads/pdf-extract/'

# RefLookup
app.config['CROSSREF_URI'] = 'http://api.crossref.org/works'
app.config['MENDELEY_SEARCH_URI'] = 'https://api.mendeley.com/search/catalog'
app.config['MENDELEY_CATALOG_URI'] = 'https://api.mendeley.com/catalog'
app.config['MENDELEY_AUTH_URI'] = 'https://api.mendeley.com/oauth/token'
app.config['MENDELEY_AUTH'] = (os.environ.get('MENDELEY_ID'), os.environ.get('MENDELEY_SECRET'))

app.config['RESULT_TTL_SECONDS'] = 300
app.secret_key = os.environ.get('REFSERVICE_SECRETKEY')

app.config['ACCESS_TOKEN_TTL'] = 300
app.config['REFRESH_TOKEN_TTL'] = 86400
app.config['API_PREFIX_V1'] = '/api/v1'
app.config['API_PREFIX_V2'] = '/api/v2'

abort_run = False
if not app.secret_key:
    print('Please define a REFSERVICE_SECRETKEY environment variable!', file=stderr)
    abort_run = True
md_id, md_secret = app.config['MENDELEY_AUTH']
if not md_id or not md_secret:
    print('Please define MENDELEY_ID and MENDELEY_SECRET environment variables!', file=stderr)
    abort_run = True
if not app.config['SCOPUS_API_KEY']:
    print('Please define a SCOPUS_API_KEY environment variable!', file=stderr)
    abort_run = True

if abort_run:
    exit(-1)


api = Api(app)
conn = Redis()

# Redis queue:
rq = Queue(connection=conn)

taskserializer = URLSafeSerializer(app.secret_key, salt='task')
tokenserializer = URLSafeTimedSerializer(app.secret_key, salt='token')

from reflookup.resources import views

if __name__ == '__main__':
    app.run(debug=True)
