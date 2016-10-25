
from flask import json
import unittest
from urllib.parse import quote

from tests.unittests import basetest


class CrossRefTest(basetest.BaseTest):
    #is the crossref endpoint works?
    def test_crossreflookup(self):
        citation = quote(self.test_cite, safe='')
        params = {'ref': citation}

        ret = self.app.post(self.prefix + '/crsearch', data=params)
        assert ret

        jdata = json.loads(ret.data)
        assert jdata
        print(jdata)

        url = jdata.get('result', None)

        assert url
        assert url[0].get('ids', None).get('doi', None) == self.cr_doi



if __name__ == '__main__':
    unittest.main()
