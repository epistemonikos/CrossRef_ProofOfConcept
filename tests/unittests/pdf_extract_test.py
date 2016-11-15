from io import BytesIO
from flask import json
import unittest
from urllib.parse import quote
from reflookup import app
import os
import requests
import time
from tests.unittests.sources.output_pdf_extract_test import result
from tests.unittests.basetest import BaseTest

class PdfExtractTest(BaseTest):

    def setUp(self):
        super(PdfExtractTest, self).setUp()
        self.pdf_path = os.path.join(os.path.dirname(__file__), 'sources/pdf_extract_test.pdf')
        self.references_path = os.path.join(os.path.dirname(__file__), 'sources/output_pdf_extract_test')
        self.pdf = open(self.pdf_path, 'rb')
        self.references = result
        self.url_base = self.prefix

    def test_pdf_extract(self):
        data = {
            'pdf_file' : (self.pdf, 'pdf_extract_test.pdf')
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
            'id' : token
        }
        while True:
            ret = self.app.get(self.url_base + '/job', data=data)
            jdata = json.loads(ret.data)
            if jdata.get('done'):
                references = jdata.get('result') or []
                import pdb; pdb.set_trace()
                self.assertEqual(references, self.references)
                break
            time.sleep(3)

if __name__ == '__main__':
    unittest.main()
