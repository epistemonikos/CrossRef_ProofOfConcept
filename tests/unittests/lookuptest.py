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

    def test_search_v2_single_query(self):
        # first cr
        params = {'q': self.test_cite}
        ret = self.app.get(self.prefix2 + '/search', data=params)
        assert ret
        jdata = json.loads(ret.data)
        assert jdata
        res = jdata.get('result', None)
        assert res
        self.assertEqual(res[0].get('ids').get('doi', None), self.cr_doi)

        # then md
        params = {'q': self.test_cite_mendeley}
        ret = self.app.get(self.prefix2 + '/search', data=params)
        assert ret
        jdata = json.loads(ret.data)
        assert jdata
        res = jdata.get('result', None)
        assert res
        assert res[0].get('ids').get('doi', None) == self.md_doi

        # then cr, but with md_only
        params = {'q': self.test_cite, 'md_only': True}
        ret = self.app.get(self.prefix2 + '/search', data=params)
        assert ret
        jdata = json.loads(ret.data)
        assert jdata
        res = jdata.get('result', None)
        assert res
        assert res[0].get('source') == 'Mendeley'

        # then md, but with cr_only
        params = {'q': self.test_cite_mendeley, 'cr_only': True}
        ret = self.app.get(self.prefix2 + '/search', data=params)
        assert ret
        jdata = json.loads(ret.data)
        assert jdata
        res = jdata.get('result', None)
        assert res
        assert res[0].get('source') == 'CrossRef'

        # then cr and return both
        params = {'q': self.test_cite, 'dont_choose': True}
        ret = self.app.get(self.prefix2 + '/search', data=params)
        assert ret
        jdata = json.loads(ret.data)
        assert jdata
        res = jdata.get('result', None)
        assert res
        assert len(res) == 2
        assert jdata.get('length', 0) == 2


if __name__ == '__main__':
    unittest.main()
