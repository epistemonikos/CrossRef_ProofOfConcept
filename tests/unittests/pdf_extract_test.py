import os
import time
import unittest

import subprocess
from flask import json

from tests.unittests.basetest import BaseTest
from tests.unittests.sources.output_pdf_extract_test import result


def pdf_exec_not_in_path():
    try:
        subprocess.call(['pdf-extract'])
        return False
    except OSError as e:
        if e.errno == os.errno.ENOENT:
            return True
        # handle file not found error.
        else:
            # Something else went wrong while trying to run `wget`
            raise


@unittest.skipIf(pdf_exec_not_in_path(), 'pdf-extract not in path.')
class PdfExtractTest(BaseTest):
    """
    This is a testing class for refs/pdf endpoint, it works with crossref gem made in ruby programming language
    """

    def setUp(self):
        """
        This is an initial method to run the testing below and the testing in other class that inherit from this class
        """
        super(PdfExtractTest, self).setUp()
        self.pdf_path = os.path.join(os.path.dirname(__file__),
                                     'sources/pdf_extract_test.pdf')
        self.references_path = os.path.join(os.path.dirname(__file__),
                                            'sources/output_pdf_extract_test')
        self.pdf = open(self.pdf_path, 'rb')
        self.references = result
        self.url_base = self.prefix

    def test_pdf_extract(self):
        """
        This test make sure the correctness and activation of pdf endpoint
        """
        data = {
            'pdf_file': (self.pdf, 'pdf_extract_test.pdf')
        }
        ret = self.app.post(
            self.url_base + '/refs/pdf',
            content_type='multipart/form-data',
            data=data,
            follow_redirects=True
        )
        assert ret
        jdata = json.loads(ret.data)
        assert jdata
        token = jdata.get('job', None)
        assert token
        data = {
            'id': token
        }
        while True:
            # busy waiting??
            ret = self.app.get(self.url_base + '/job', data=data)
            jdata = json.loads(ret.data)
            if jdata.get('done'):
                references = jdata.get('result') or []
                self.assertEqual(references, self.references)
                break
            time.sleep(3)


if __name__ == '__main__':
    unittest.main()
