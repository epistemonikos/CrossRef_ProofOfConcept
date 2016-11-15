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
        self.url_base = 'http://0.0.0.0:5001'

    def test_pdf_extract(self):
        files = {
            'pdf_file' : self.pdf
        }
        ret = requests.post(self.url_base + self.prefix + '/refs/pdf', files=files)
        assert ret
        jdata = ret.json()
        assert jdata
        token = jdata.get('job', None)
        assert token
        data = {
            'id' : token
        }
        while True:
            ret = requests.get(self.url_base + '/api/v1/job', data=data)
            jdata = ret.json()
            if jdata.get('done'):
                references = jdata.get('result') or []
                self.assertEqual(references, self.references)
                break
            time.sleep(3)

if __name__ == '__main__':
    unittest.main()
