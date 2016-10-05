from flask import Flask
from flask_restful import Api
import os

app = Flask(__name__)

app.config['CROSSREF_URI'] = 'http://api.crossref.org/works'
app.config['MENDELEY_URI'] = 'https://api.mendeley.com/search/catalog'
app.config['MENDELEY_AUTH'] = ('3578', 'y43xcFyn1lNG7VT5')  # TODO: MOVE TO ENV
app.config['MENDELEY_AUTH_URI'] = 'https://api.mendeley.com/oauth/token'


app.secret_key = os.environ.get('REFSERVICE_SECRETKEY', '12345')
app.config['API_PREFIX'] = '/api/v1'
api = Api(app)

from reflookup import views


if __name__ == '__main__':
    app.run(debug=True)
