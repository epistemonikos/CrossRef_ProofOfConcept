import unittest

from flask import json

from tests.unittests import basetest


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

    def test_mendeleycrash(self):
        params = {'ref' : 'msdlknfgskdlamnfkasd njsdn sdnvkfsnxnjvjjvxsfjv sdkjv ksjd  '}
        ret = self.app.post(self.prefix + '/mdsearch', data=params)
        assert ret
        assert ret.status_code == 404

if __name__ == '__main__':
    unittest.main()
