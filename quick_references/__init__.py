import os

from flask import Flask
from flask_restful import Api

app = Flask(__name__)

app.config['SCOPUS_URI'] = 'https://api.elsevier.com/content/article/doi/'
app.config['SCOPUS_API_KEY'] = 'd1dd2bfada7ec327c3f4a3e316ec98b8'
app.config['SCOPUS_DTD'] = {
        "default": "http://www.elsevier.com/xml/svapi/article/dtd",
        "sb": "http://www.elsevier.com/xml/common/struct-bib/dtd",
        "ce": "http://www.elsevier.com/xml/common/dtd",
    }

app.config['RESULT_TTL_SECONDS'] = 300
app.secret_key = os.environ.get('REFSERVICE_SECRETKEY', '12345')
app.config['API_PREFIX'] = '/api/v1'
api = Api(app)


if __name__ == '__main__':
    app.run(debug=True)
