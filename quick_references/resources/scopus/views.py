import requests
from quick_references import app
from quick_references.utils.standardize_json import scopus_to_standard

from urllib.parse import unquote
from flask_restful import reqparse, Resource

from werkzeug.exceptions import abort


"""
This file contains the endpoint resources for retrieving references from Scopus
"""


class ScopusResource(Resource):
    """
        This resource represents the /refs/scopus endpoint on the API.
    """

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('doi', type=str, required=True,
                                 location='values')

    def get(self):
        data = self.parser.parse_args()
        doi = unquote(data['doi']).strip()
        return self.retrieve_references(doi)

    def post(self):
        return self.get()

    def retrieve_references(self, doi):
        params = {
            "apiKey": app.config["SCOPUS_API_KEY"]
        }
        headers = {
            "Accept": "text/xml"
        }
        resp = requests.get(app.config["SCOPUS_URI"] + doi, params=params, headers=headers)

        if resp.status_code == 200:
            return scopus_to_standard(resp.text)
        elif resp.status_code == 404:
            abort(404, 'Resource not found.')
        else:
            abort(resp.status_code, "Couldn't retrieve references for DOI:" + doi)
