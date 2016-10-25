import unittest

from flask import json
import tests.unittests.basetest

from urllib.parse import quote

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

if __name__ == '__main__':
    unittest.main()
