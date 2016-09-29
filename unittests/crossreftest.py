import unittest

from flask import json

import unittests.basetest
from urllib.parse import quote


class CrossRefTest(unittests.basetest.BaseTest):
    def test_crossreflookup(self):
        citation = quote(self.test_cite, safe='')
        params = {'ref': citation}

        ret = self.app.post(self.prefix + '/crsearch', data=params)
        assert ret

        jdata = json.loads(ret.data)
        assert jdata

        url = jdata.get('URL', None)
        assert url
        assert url == self.cr_doi


if __name__ == '__main__':
    unittest.main()
