import unittest

from flask import json
from tests.unittests import basetest


class LookupTest(basetest.BaseTest):
    #this test check an especial reference where crossref service must win
    def test_lookup(self):
        params = {'ref': self.test_cite}
        ret = self.app.post(self.prefix + '/search', data=params)
        assert ret
        jdata = json.loads(ret.data)
        assert jdata
        res = jdata.get('result', None)
        assert res
        self.assertEqual(res[0].get('ids').get('doi', None), self.cr_doi)

    def test_lookup2(self):
        # this test check an especial reference where mendeley service must win
        params = {'ref': self.test_cite_mendeley}
        ret = self.app.post(self.prefix + '/search', data=params)
        assert ret
        jdata = json.loads(ret.data)
        assert jdata
        res = jdata.get('result', None)
        assert res
        assert res[0].get('ids').get('doi', None) == self.md_doi

if __name__ == '__main__':
    unittest.main()
