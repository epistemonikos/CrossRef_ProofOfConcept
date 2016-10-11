from datetime import datetime

import requests
from flask_restful import Resource, reqparse
from werkzeug.exceptions import abort

from reflookup import app
from reflookup.standardize_json import mendeley_to_standard

"""
This file contains the endpoint resources for looking up references in
Mendeley.
"""


def mendeley_lookup(citation):
    params = {'query': citation}
    # Note that Mendeley requires authentication:
    headers = {
        'Authorization': 'Bearer ' + MendeleyLookupResource.get_access_token(),
        'Accept': 'application/vnd.mendeley-document.1+json'
    }
    res = requests.get(app.config['MENDELEY_URI'],
                       params=params, headers=headers)

    return mendeley_to_standard(res.json())


class MendeleyLookupResource(Resource):
    """
        This resource represents the /mdsearch endpoint on the API.
        """

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('ref', type=str, required=True,
                                 location='values')

    def get(self):
        citation = self.parser.parse_args().get('ref')
        return mendeley_lookup(citation)

    def post(self):
        return self.get()

    @staticmethod
    def get_access_token():
        """
        Helper function. Verifies the status of the current access token and
        renews it if necessary, storing it.
        TODO: Fix errors related to Mendeley not returning an access token.
        :return: A valid access token.
        """
        token = app.config.get('MENDELEY_ACCESS_TOKEN')
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
        """
        Calls the Mendeley API to renew the access token and stores it.
        :return: A new access token.
        """
        r = requests.post(app.config['MENDELEY_AUTH_URI'],
                          data={'grant_type': 'client_credentials',
                                'scope': 'all'},
                          auth=app.config['MENDELEY_AUTH'])

        if r.status_code == 200:
            app.config['MENDELEY_ACCESS_TOKEN'] = {
                'token': r.json()['access_token'],
                'expires_in': r.json()['expires_in'],
                'created': datetime.now()
            }

            return app.config['MENDELEY_ACCESS_TOKEN']

        abort(500, 'Error when renewing Mendeley access token.')
