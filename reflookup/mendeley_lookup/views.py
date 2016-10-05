##Request para obtener access_token
import requests
from datetime import datetime
from flask import render_template, make_response, json
from flask_restful import Resource, reqparse
from werkzeug.utils import redirect

from reflookup import app, api
from reflookup.search_form import CrossRefForm

from urllib.parse import unquote
from requests.auth import HTTPBasicAuth

def get_access_token():
    token = app.config["mendeley_access_token"]
    then = app.config["token_generation_time"]
    delta = app.config["token_expires_in"] - 100
    now = datetime.now()
    if token == "" | (then - now).total_seconds() > delta :
        r = requests.post(app.config["mendeley_url"],
                          data={'grant_type': 'client_credentials', 'scope': 'all'},
                          auth=('3578', 'y43xcFyn1lNG7VT5'))
        app.config["mendeley_access_token"] = r.json()["access_token"]
        app.config["token_expires_in"] = r.json()["expires_in"]
        app.config["token_generation_time"] = datetime.now()
    return app.config["mendeley_access_token"]

@app.route("/mendeley/<citation>")
def citation_lookup(citation):
    params = {'query' : citation}
    headers = {
        'Authorization' : "Bearer " + get_access_token(),
        "Accept" : 'application/vnd.mendeley-document.1+json'
    }
    res = requests.get('https://api.mendeley.com/search/catalog', params=params, headers=headers)
    #req["rating"] = Rating(citation, result).value()
    return res.json()
