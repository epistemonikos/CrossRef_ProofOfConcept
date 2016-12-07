from flask_restful import Resource
from flask_restful.reqparse import RequestParser
from reflookup.auth.models import User
from reflookup import app


class RefreshTokenResource(Resource):
    """
    Endpoint for renewing access tokens.
    """

    def __init__(self):
        self.parser = RequestParser()
        self.parser.add_argument('access_token', type=str, required=True)
        self.parser.add_argument('refresh_token', type=str, required=True)

    def post(self):
        args = self.parser.parse_args()
        (a_token, r_token) = User.refresh_access_token(args['access_token'],
                                                       args['refresh_token'])

        return {
            'access_token': a_token,
            'refresh_token': r_token,
            'token_ttl': app.config.get('ACCESS_TOKEN_TTL')
        }


class LoginResource(Resource):

    def __init__(self):
        self.parser = RequestParser()
        self.parser.add_argument('email', type=str, required=True)
        self.parser.add_argument('password', type=str, required=True)

    def post(self):
        args = self.parser.parse_args()

        (a_token, r_token) = User.get_access_token(args['email'], args['password'])

        return {
            'access_token': a_token,
            'refresh_token': r_token,
            'token_ttl': app.config.get('ACCESS_TOKEN_TTL')
        }
