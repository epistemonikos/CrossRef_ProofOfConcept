import time
import unittest

import hashlib
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
        ret = self.app.post(self.prefix + '/search', query_string=params)
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
        ret = self.app.post(self.prefix + '/search', query_string=params)
        assert ret
        jdata = json.loads(ret.data)
        assert jdata
        res = jdata.get('result', None)
        assert res
        assert res[0].get('ids').get('doi', None) == self.md_doi

    def test_search_v2_single_query(self):
        cr_md5 = hashlib.md5(self.test_cite.encode('utf-8')).hexdigest()
        md_md5 = hashlib.md5(self.test_cite_mendeley.encode('utf-8')).hexdigest()

        # first cr
        params = {'q': self.test_cite, 'sync': True}
        ret = self.app.get(self.prefix2 + '/search', query_string=params)
        assert ret
        jdata = json.loads(ret.data)
        assert jdata
        res = jdata.get('result', None)
        assert res
        self.assertEqual(res[0].get('ids').get('doi', None), self.cr_doi)
        self.assertEqual(res[0].get('md5'), cr_md5)

        # then md
        params = {'q': self.test_cite_mendeley, 'sync': True}
        ret = self.app.get(self.prefix2 + '/search', query_string=params)
        assert ret
        jdata = json.loads(ret.data)
        assert jdata
        res = jdata.get('result', None)
        assert res
        assert res[0].get('ids').get('doi', None) == self.md_doi
        self.assertEqual(res[0].get('md5'), md_md5)

        # then cr, but with md_only
        params = {'q': self.test_cite, 'md_only': True, 'sync': True}
        ret = self.app.get(self.prefix2 + '/search', query_string=params)
        assert ret
        jdata = json.loads(ret.data)
        assert jdata
        res = jdata.get('result', None)
        assert res
        assert res[0].get('source') == 'Mendeley'

        # then md, but with cr_only
        params = {'q': self.test_cite_mendeley, 'cr_only': True, 'sync': True}
        ret = self.app.get(self.prefix2 + '/search', query_string=params)
        assert ret
        jdata = json.loads(ret.data)
        assert jdata
        res = jdata.get('result', None)
        assert res
        assert res[0].get('source') == 'CrossRef'

    def test_search_v2_deferred_queries(self):
        params = {'q': [self.test_cite, self.test_cite_mendeley]}

        ret = self.app.get(self.prefix2 + '/search', query_string=params)
        assert ret

        jdata = json.loads(ret.data)
        assert jdata
        job_id = jdata.get('job')
        assert job_id

        for i in range(0, 10):
            time.sleep(2)

            ret = self.app.get(self.prefix + '/job',
                               query_string={'id': job_id})
            assert ret

            jdata = json.loads(ret.data)
            assert jdata
            if jdata.get('done', False):
                break

            self.assertLess(i, 10, msg='Exceeded timeout for job completion.')

        self.assertLess(0, jdata.get('length', 0),
                        msg='Job returned with error.'
                            ' Length = {}, Error = {}'.format(
                            jdata.get('length'), jdata.get('result')))

        result = jdata.get('result', None)
        self.assertEqual(type(result), list)

        for r in result:
            self.assertTrue(
                r.get('ids', {}).get('doi') in {self.cr_doi, self.md_doi})


if __name__ == '__main__':
    unittest.main()
