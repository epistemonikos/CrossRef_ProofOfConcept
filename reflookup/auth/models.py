from flask.ext.restful import abort

from reflookup import db, tokenserializer
from itsdangerous import BadSignature, SignatureExpired
from enum import Enum
from datetime import datetime
from uuid import uuid1
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.hashes import Hash, SHA256


class Scopes(Enum):
    client = 'client'
    admin = 'admin'


class Client(db.Model):
    __tablename__ = 'clients'
    id = db.Column(db.Integer, primary_key=True)
    scope = db.Column(db.Enum(Scopes), nullable=False, default=Scopes.client)
    mail = db.Column(db.String, nullable=False)
    renew_token = db.Column(db.B, nullable=True, default=None, unique=True)

    created = db.Column(db.Date, default=datetime.now)
    modified = db.Column(db.Date, default=datetime.now, onupdate=datetime.now)

    def __init__(self, mail, scope=Scopes.client):
        self.mail = mail
        self.scope = scope

    def renew_access_token(self, renew_token=None):
        """
        Returns a new access and renew token pair.
        :return: A tuple containing the access token and a renew token.
        """

        def create_tokens():
            atoken = tokenserializer.dumps({'client': self.id})
            rtoken = uuid1().bytes

            h = Hash(SHA256(), backend=default_backend())
            h.update(rtoken)
            self.renew_token = h.finalize()

            db.session.add(self)
            db.session.commit()

            return (tokenserializer.dumps(atoken),
                    tokenserializer.dumps(rtoken))

        if not self.renew_token:
            return create_tokens()
        else:
            if not renew_token:
                abort(401, message='Please provide a renew token.')

            try:
                renew_token = tokenserializer.loads(renew_token)

                h = Hash(SHA256(), backend=default_backend())
                h.update(renew_token)
                renew_token = h.finalize()

                if renew_token != self.renew_token:
                    abort(401, message='Invalid renew token.')
            except BadSignature:
                abort(401, message='Invalid renew token.')

    @staticmethod
    def validate_access_token(access_token, access_scope=Scopes.client):
        try:
            token = tokenserializer.loads(access_token, max_age=300)
            client_id = token.get('client', None)
            if not client_id:
                raise BadSignature('Token does not contain a client ID.')

            client = Client.query.filter(Client.id == client_id).first()
            if not client:
                raise BadSignature('No such client.')

            if client.scope != access_scope and client.scope != Scopes.admin:
                abort(403, message='Insufficient Privileges.')

        except SignatureExpired:
            abort(401, message='Expired access token.')
        except BadSignature:
            abort(401, message='Bad access token.')
        except:
            raise

