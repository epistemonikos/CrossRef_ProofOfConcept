import unittest

from flask import json
from tests.unittests import basetest


class LookupTest(basetest.BaseTest):
    """
        This Test class check the /search endpoint.
    """
    def test_lookup(self):
        """
            This test check an especial reference where crossref service must win
        """
        params = {'ref': self.test_cite}
        ret = self.app.post(self.prefix + '/search', data=params)
        assert ret
        jdata = json.loads(ret.data)
        assert jdata
        res = jdata.get('result', None)
        assert res
        self.assertEqual(res[0].get('ids').get('doi', None), self.cr_doi)

    def test_lookup2(self):
        """
        This test check an especial reference where mendeley service must win
        """
        params = {'ref': self.test_cite_mendeley}
        ret = self.app.post(self.prefix + '/search', data=params)
        assert ret
        jdata = json.loads(ret.data)
        assert jdata
        res = jdata.get('result', None)
        assert res
        assert res[0].get('ids').get('doi', None) == self.md_doi

    def test_searchv2(self):
        params = {'ref': self.test_cite}
        ret = self.app.post(self.prefix + '/search', data=params)
        assert ret
        jdata = json.loads(ret.data)
        assert jdata
        res = jdata.get('result', None)
        assert res
        self.assertEqual(res[0].get('ids').get('doi', None), self.cr_doi)

if __name__ == '__main__':
    unittest.main()
