import os
from datetime import datetime
from functools import wraps

from flask import request
from flask_restful import abort
from itsdangerous import BadSignature, SignatureExpired
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.hashes import Hash, SHA256

from reflookup import db, tokenserializer, app

scopes = {
    'admin': 0,
    'client': 1
}


# Function for token generation.
def create_tokens(owner):
    serial_code = int.from_bytes(os.urandom(4), byteorder="big")

    atoken = {
        'type': 'access_token',
        'client': owner.id,
        'scope': owner.scope,
        'serial': serial_code
    }

    rtoken = {
        'type': 'refresh_token',
        'client': owner.id,
        'serial': serial_code
    }

    owner.token_serial = serial_code

    db.session.add(owner)
    db.session.commit()

    return tokenserializer.dumps(atoken), tokenserializer.dumps(rtoken)


# --------------------------------------


def auth_required(scope=scopes['client']):
    def decorator(view):
        @wraps(view)
        def wrapper(*args, **kwargs):
            if app.debug or app.testing:
                return view(*args, **kwargs)

            token = request.headers.get('Authorization').split(' ')[1]
            User.validate_access_token(token, scope)

            return view(*args, **kwargs)

        return wrapper

    return decorator


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    scope = db.Column(db.Integer, nullable=False, default=scopes['client'])
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)

    token_serial = db.Column(db.Integer, nullable=True, default=None)

    created = db.Column(db.Date, default=datetime.now)
    modified = db.Column(db.Date, default=datetime.now, onupdate=datetime.now)

    def __init__(self, mail, password, scope=scopes['client']):
        self.email = mail
        self.scope = scope

        h = Hash(SHA256(), default_backend())
        h.update(password.encode('utf-8'))

        self.password = h.finalize()

    @staticmethod
    def get_access_token(email, password):
        """
        Forces creation of new access and refresh token pair.
        :return:
        """

        user = User.query.filter(User.email == email).first()
        if not user:
            abort(401)

        h = Hash(SHA256(), default_backend())
        h.update(password.encode('utf-8'))
        h_pass = h.finalize()

        if not user.password == h_pass:
            abort(401)

        return create_tokens(user)

    @staticmethod
    def refresh_access_token(access_token, refresh_token):
        """
        Returns a new access and refresh token pair.
        :return: A tuple containing the access token and a refresh token.
        """

        try:
            token = tokenserializer.loads(access_token)
            client_id = token.get('client', None)
            if not client_id:
                print('No client ID.')
                raise BadSignature('Access token does not contain a client ID.')

            client = User.query.filter(User.id == client_id).first()
            if not client:
                print('No valid client.')
                raise BadSignature('No such client.')

            if not refresh_token:
                abort(401, message='Please provide a refresh token.')

            try:
                refresh_token = tokenserializer.loads(refresh_token)
                refresh_serial = refresh_token.get('serial')
                refresh_client = refresh_token.get('client')

                if refresh_serial != token.get('serial') != client.token_serial or refresh_client != client_id != client.id:
                    abort(403, message='Invalid refresh token.')

                return create_tokens(client)

            except BadSignature:
                abort(403, message='Invalid refresh token.')
            except:
                raise

        except BadSignature:
            print('Error deserializing.')
            abort(403, message='Bad access token.')
        except:
            raise

    @staticmethod
    def validate_access_token(access_token, access_scope=scopes['client']):
        try:
            token = tokenserializer.loads(access_token, max_age=app.config.get(
                'ACCESS_TOKEN_TTL'))
            client_id = token.get('client', None)
            if not client_id:
                raise BadSignature('Token does not contain a client ID.')

            client = User.query.filter(User.id == client_id).first()
            if not client:
                raise BadSignature('No such client.')

            if token.get('scope') > access_scope:
                abort(403, message='Insufficient Privileges.')

        except SignatureExpired:
            abort(401, message='Expired access token.')
        except BadSignature:
            abort(401, message='Bad access token.')
        except:
            raise
