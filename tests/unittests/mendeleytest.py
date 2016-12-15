import unittest

from flask import json

from tests.unittests import basetest


class MendeleyTest(basetest.BaseTest):
    """
    This is a testing class for mdsearch endpoint, it works with mendeley API
    """
    def test_mendeleylookup(self):
        """
            This test make sure the correctness and activation of mdsearch endpoint
        """
        params = {'ref': self.test_cite_mendeley}
        ret = self.app.post(self.prefix + '/mdsearch', data=params)
        assert ret
        jdata = json.loads(ret.data)
        assert jdata
        url = jdata.get('result', None)

        assert url
        assert url[0].get('ids', None).get('doi',None) == self.md_doi

    def test_mendeleycrash(self):
        """
            This test probe an incorrect input on mdsearch endpoint, and expect an 404 HTTP response code
        """
        params = {'ref' : 'msdlknfgskdlamnfkasd njsdn sdnvkfsnxnjvjjvxsfjv sdkjv ksjd  '}
        ret = self.app.post(self.prefix + '/mdsearch', data=params)
        assert ret
        assert ret.status_code == 404

if __name__ == '__main__':
    unittest.main()
