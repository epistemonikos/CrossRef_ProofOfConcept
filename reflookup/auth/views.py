from flask_restful import Resource
from flask_restful.reqparse import RequestParser
from reflookup.auth.models import Client
from reflookup import app


class AuthResource(Resource):
    """
    Endpoint for renewing access tokens.
    """

    def __init__(self):
        self.parser = RequestParser()
        self.parser.add_argument('access_token', type=str, required=True)
        self.parser.add_argument('renew_token', type=str, required=True)

    def get(self):
        args = self.parser.parse_args()
        (a_token, r_token) = Client.renew_access_token(
            access_token=args['access_token'],
            renew_token=args['renew_token'])

        return {
            'access_token': a_token,
            'renew_token': r_token,
            'token_ttl': app.config.get('ACCESS_TOKEN_TTL')
        }
