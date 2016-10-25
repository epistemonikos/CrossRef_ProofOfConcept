import unittest

from flask import json
import tests.unittests.basetest

from urllib.parse import quote

class MendeleyTest(tests.unittests.basetest.BaseTest):
    def test_mendeleylookup(self):
        citation = quote(self.test_cite_mendeley, safe='')
        params = {'ref': citation}
        ret = self.app.post(self.prefix + '/mdsearch', data=params)
        assert ret
        jdata = json.loads(ret.data)
        assert jdata
        url = jdata.get('ids', None)
        if url:
            url = url.get('doi',None)
        assert url
        assert url == self.md_doi

if __name__ == '__main__':
    unittest.main()
