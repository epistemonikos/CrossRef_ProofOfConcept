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

    def test_crossreflookup_ris(self):
        citation = quote(self.test_cite, safe='')
        params = {'ref': citation}
        headers={'Accept' : 'application/x-research-info-systems'}

        ret = self.app.post(self.prefix + '/crsearch', data=params,
                            headers=headers)

        assert ret.headers['Content-Type'] == 'application/x-research-info-systems'


if __name__ == '__main__':
    unittest.main()
