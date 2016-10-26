import unittest
from flask import json
from tests.unittests import basetest
from reflookup.resources import lookup_functions

class MendeleyTest(basetest.BaseTest):
    def test_mendeleylookup(self):
        params = {'ref': self.test_cite_mendeley}
        ret = self.app.post(self.prefix + '/mdsearch', data=params)
        assert ret
        jdata = json.loads(ret.data)
        assert jdata
        url = jdata.get('result', None)

        assert url
        assert url[0].get('ids', None).get('doi',None) == self.md_doi

    def test_access_token(self):
        #This test verifies the correct upgrade the API requires "access_token"
        token_old = lookup_functions.get_mendeley_access_token()
        assert token_old
        token_new = lookup_functions.refresh_mendeley_token()
        assert token_new
        assert token_old != token_new

if __name__ == '__main__':
    unittest.main()
