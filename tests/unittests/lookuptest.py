import unittest

from flask import json
import tests.unittests.basetest

from urllib.parse import quote

class LookupTest(tests.unittests.basetest.BaseTest):
    #this test check an especial reference where crossref service must win
    def test_lookup(self):
        citation = quote(self.test_cite, safe='')
        params = {'ref': citation}
        ret = self.app.post(self.prefix + '/search', data=params)
        assert ret
        jdata = json.loads(ret.data)
        assert jdata
        url = jdata.get('ids', None)
        if url:
            url = url.get('doi',None)
        assert url
        assert url == self.cr_doi

if __name__ == '__main__':
    unittest.main()
