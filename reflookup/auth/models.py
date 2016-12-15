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


# --------------------------------------


def auth_required(scope=scopes['client']):
    def decorator(view):

        @wraps(view)
        def wrapper(*args, **kwargs):

            if app.testing:
                return view(*args, **kwargs)

            auth = request.headers.get('Authorization')
            if not auth:
                abort(401)

            try:
                token = auth.split(' ')

                if token[0] != 'Bearer':
                    abort(401, message='Malformed Authorization header.')

                User.validate_access_token(token[1], scope)
            except AttributeError:
                abort(401, message='Malformed Authorization header.')
            except:
                raise

            return view(*args, **kwargs)

        return wrapper

    return decorator


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    scope = db.Column(db.Integer, nullable=False, default=scopes['client'])
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)

    token = db.Column(db.String, nullable=True)

    created = db.Column(db.Date, default=datetime.now)
    modified = db.Column(db.Date, default=datetime.now, onupdate=datetime.now)

    def __init__(self, mail, password, scope=scopes['client']):
        self.email = mail
        self.scope = scope

        h = Hash(SHA256(), default_backend())
        h.update(password.encode('utf-8'))

        self.password = h.finalize()

    # Function for token generation.
    def create_token(self):
        a_token = {
            'type': 'access_token',
            'client': self.id,
            'scope': self.scope,
        }

        token_ser = tokenserializer.dumps(a_token)

        h = Hash(SHA256(), default_backend())
        h.update(token_ser.encode('utf-8'))

        self.token = h.finalize()

        db.session.add(self)
        db.session.commit()

        return token_ser

    @staticmethod
    def validate_access_token(access_token, access_scope=scopes['client']):
        try:
            token = tokenserializer.loads(access_token)
            client_id = token.get('client', None)
            if not client_id:
                raise BadSignature('Token does not contain a client ID.')

            client = User.query.filter(User.id == client_id).first()
            if not client:
                raise BadSignature('No such client.')

            h = Hash(SHA256(), default_backend())
            h.update(access_token.encode('utf-8'))

            if not client.token == h.finalize():
                abort(401, message='Invalid access token.')

            if token.get('scope') > access_scope:
                abort(403, message='Insufficient Privileges.')

        except SignatureExpired:
            abort(401, message='Expired access token.')
        except BadSignature:
            abort(401, message='Bad access token.')
        except:
            raise

    @staticmethod
    def login(email, password):

        user = User.query.filter(User.email == email).first()

        h = Hash(SHA256(), default_backend())
        h.update(password.encode('utf-8'))

        if not user.password == h.finalize():
            return None
        else:
            return user
