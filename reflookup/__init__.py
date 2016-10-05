from flask import Flask
from flask_restful import Api
import os

app = Flask(__name__)
app.config['CROSSREF_URI'] = 'http://api.crossref.org/works'
app.secret_key = os.environ.get('REFSERVICE_SECRETKEY', '12345')
app.config['API_PREFIX'] = '/api/v1'
api = Api(app)

from reflookup import views


if __name__ == '__main__':
    app.run(debug=True)
