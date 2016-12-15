import unittest

from flask import json

from tests.unittests.basetest import BaseTest
from reflookup import db, app
from reflookup.auth.models import User


class AuthTest(BaseTest):
    def setUp(self):
        super().setUp()

        self.email = 'darth@sidius.org'
        self.passwd = 'EmpireDidNothingWrong'

        self.user = User(mail=self.email, password=self.passwd)
        db.session.add(self.user)
        db.session.commit()

        self.token = self.user.create_token()

    def tearDown(self):
        db.session.delete(self.user)
        db.session.commit()

    def test_access_protected_resource(self):
        # this is necessary to ensure everything auth-related is tested
        # correctly, since the app normally disables auth verification
        # when testing.
        app.testing = False

        # first, test that access is denied if no auth info is provided

        rv = self.app.get(self.prefix2 + '/search', query_string={'q': 'foo'})
        self.assertEqual(rv.status_code, 401)

        # second, test that access is denied if wrong auth header is provided
        rv = self.app.get(self.prefix2 + '/search',
                          query_string={'q': 'foo'},
                          headers={'Authorization': 'blah blah'})
        self.assertEqual(rv.status_code, 401)

        rv = self.app.get(self.prefix2 + '/search',
                          query_string={'q': 'foo'},
                          headers={'Authorization': self.token})
        self.assertEqual(rv.status_code, 401)

        # finally, test correct authorization
        rv = self.app.get(self.prefix2 + '/search',
                          query_string={'q': 'foo'},
                          headers={
                              'Authorization': 'Bearer {}'.format(self.token)
                          })
        self.assertEqual(rv.status_code, 202)

        app.testing = True


if __name__ == '__main__':
    unittest.main()
