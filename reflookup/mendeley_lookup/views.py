from datetime import datetime
from urllib.parse import unquote

import requests
from flask_restful import reqparse
from reflookup.restful_utils.utils import ExtResource
from werkzeug.exceptions import abort

from rating.rating import Rating
from reflookup import app
from reflookup.standardize_json import mendeley_to_standard

"""
This file contains the endpoint resources for looking up references in
Mendeley.
"""


def mendeley_lookup(citation, return_all=False):
    params = {'query': citation}
    # Note that Mendeley requires authentication:
    headers = {
        'Authorization': 'Bearer ' + MendeleyLookupResource.get_access_token(),
        'Accept': 'application/vnd.mendeley-document.1+json'
    }
    req = requests.get(app.config['MENDELEY_URI'],
                       params=params, headers=headers)

    if req.status_code != 200:
        if req.status_code == 401:
            MendeleyLookupResource.refresh_token()
            return mendeley_lookup(citation)
        else:
            abort(req.status_code, 'Remote API error.')

    rv = req.json()

    if len(rv) < 1:
        abort(404, 'No results found for query.')

    if return_all:
        result = []
        for r in rv:
            std = mendeley_to_standard(r)
            std['rating'] = Rating(citation, std).value()
            result.append(std)
        return result

    else:
        result = rv[0]
        result = mendeley_to_standard(result)
        result['rating'] = Rating(citation, result).value()
        return result


class MendeleyLookupResource(ExtResource):
    """
        This resource represents the /mdsearch endpoint on the API.
        """

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('ref', type=str, required=True,
                                 location='values')

    def get(self):
        data = self.parser.parse_args()
        ref = unquote(data['ref']).strip()
        return mendeley_lookup(ref)

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
        else:
            then = token['created']
            delta = token['expires_in'] - 100
            now = datetime.now()
            if (now - then).total_seconds() > delta:
                token = MendeleyLookupResource.refresh_token()
        return token['token']

    @staticmethod
    def refresh_token():
        """
        Calls the Mendeley API to renew the access token and stores it.
        :return: A new access token.
        """
        print("Renovando Token")
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
