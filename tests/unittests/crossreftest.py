
from flask import json
import unittest
from urllib.parse import quote

from tests.unittests import basetest


class CrossRefTest(basetest.BaseTest):
    def test_crossreflookup(self):
        citation = quote(self.test_cite, safe='')
        params = {'ref': citation}

        ret = self.app.post(self.prefix + '/crsearch', data=params)
        assert ret

        jdata = json.loads(ret.data)
        assert jdata

        url = jdata.get('ids', None)
        assert url
        assert url.get('doi', None) == self.cr_doi



if __name__ == '__main__':
    unittest.main()
