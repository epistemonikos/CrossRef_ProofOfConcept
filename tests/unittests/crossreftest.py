
from flask import json
import unittest
from urllib.parse import quote

from tests.unittests import basetest


class CrossRefTest(basetest.BaseTest):
    """
    This is a testing class for crsearch endpoint, it works with crossref API
    """
    def test_crossreflookup(self):
        """
        This test make sure the correctness and activation of crsearch endpoint
        """
        citation = quote(self.test_cite, safe='')
        params = {'ref': citation}

        ret = self.app.post(self.prefix + '/crsearch', data=params)
        assert ret
        jdata = json.loads(ret.data)
        assert jdata
        url = jdata.get('result', None)
        assert url
        self.assertEqual(url[0].get('ids', None).get('doi', None), self.cr_doi)

    def test_crossrefcrash(self):
        """
        This test probe an incorrect input on crsearch endpoint, and expect an 404 HTTP response code
        """
        params = {'ref': 'kangfkadslnfklasdmnfglkamfklafñlmnadlkfmsaklf'}
        ret = self.app.post(self.prefix + '/crsearch', data=params)
        assert ret
        assert ret.status_code == 404


if __name__ == '__main__':
    unittest.main()
