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

    def tearDown(self):
        db.session.delete(self.user)
        db.session.commit()

    def test_login(self):
        params = {'email': self.email, 'password': self.passwd}
        rv = self.app.post(self.prefix2 + '/login', query_string=params)

        self.assertEqual(rv.status_code, 200)
        jdata = json.loads(rv.data)
        assert jdata
        assert jdata.get('access_token')
        assert jdata.get('refresh_token')

    def test_refresh_token(self):
        params = {'email': self.email, 'password': self.passwd}
        rv = self.app.post(self.prefix2 + '/login', query_string=params)
        jdata = json.loads(rv.data)

        a_token = jdata.get('access_token')
        r_token = jdata.get('refresh_token')

        params = {'access_token': a_token, 'refresh_token': r_token}
        rv = self.app.post(self.prefix2 + '/renew_access', query_string=params)

        self.assertEqual(rv.status_code, 200)
        jdata = json.loads(rv.data)
        assert jdata
        assert jdata.get('access_token')
        assert jdata.get('refresh_token')
        self.assertNotEqual(a_token, jdata.get('access_token'))
        self.assertNotEqual(r_token, jdata.get('refresh_token'))

    def test_access_protected_resource(self):
        # this is necessary to ensure everything auth-related is tested
        # correctly, since the app normally disables auth verification
        # when testing.
        app.testing = False

        params = {'email': self.email, 'password': self.passwd}
        rv = self.app.post(self.prefix2 + '/login', query_string=params)
        jdata = json.loads(rv.data)

        a_token = jdata.get('access_token')

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
                          headers={'Authorization': a_token})
        self.assertEqual(rv.status_code, 401)

        # finally, test correct authorization
        rv = self.app.get(self.prefix2 + '/search',
                          query_string={'q': 'foo'},
                          headers={
                              'Authorization': 'Bearer {}'.format(a_token)
                          })
        self.assertEqual(rv.status_code, 202)

        app.testing = True


if __name__ == '__main__':
    unittest.main()
