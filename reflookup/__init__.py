from flask import Flask
from flask_restful import Api

app = Flask(__name__)
app.config['CROSSREF_URI'] = 'http://api.crossref.org/works'
app.secret_key = 'blah blah'  # TODO: Replace with real, pseudorandom, string
app.config['API_PREFIX'] = '/api/v1'
api = Api(app)


@app.route('/')
def root():
    return 'Hello World!'

from reflookup import views


if __name__ == '__main__':
    app.run()
