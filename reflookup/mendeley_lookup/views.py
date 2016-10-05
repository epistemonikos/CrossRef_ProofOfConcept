from datetime import datetime
from flask_restful import Resource, reqparse

import requests
from werkzeug.exceptions import abort

from reflookup import app


class MendeleyLookupResource(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('ref', type=str, required=True,
                                 location='values')

    def get(self):
        citation = self.parser.parse_args().get('ref')
        params = {'query': citation}
        headers = {
            'Authorization': "Bearer " + self.get_access_token(),
            "Accept": 'application/vnd.mendeley-document.1+json'
        }
        res = requests.get(app.config['MENDELEY_URI'],
                           params=params, headers=headers)
        # req["rating"] = Rating(citation, result).value()
        # TODO: Fix rating to work with Mendeley.
        # TODO: Fix RIS parser to work with Mendeley.
        # TODO: Standardize JSON.
        return res.json()

    def post(self):
        return self.get()

    @staticmethod
    def get_access_token():
        token = app.config.get("MENDELEY_ACCESS_TOKEN")
        if not token:
            token = MendeleyLookupResource.refresh_token()

        then = token['created']
        delta = token['expires_in'] - 100
        now = datetime.now()
        if (then - now).total_seconds() > delta:
            token = MendeleyLookupResource.refresh_token()

        return token['token']

    @staticmethod
    def refresh_token():
        r = requests.post(app.config["MENDELEY_AUTH_URI"],
                          data={'grant_type': 'client_credentials',
                                'scope': 'all'},
                          auth=app.config['MENDELEY_AUTH'])

        if r.status_code == 200:
            app.config['MENDELEY_ACCESS_TOKEN'] = {
                'token': r.json()["access_token"],
                'expires_in': r.json()["expires_in"],
                'created': datetime.now()
            }

            return app.config['MENDELEY_ACCESS_TOKEN']

        abort(500, 'Error when renewing Mendeley access token.')
