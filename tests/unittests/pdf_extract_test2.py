from flask import json
import unittest
from urllib.parse import quote
from reflookup import app
import os
import requests
import time
from tests.unittests.sources.output_pdf_extract_test import result

class PdfExtractTest(unittest.TestCase):
    __module__ = __name__
    __qualname__ = 'PdfExtractTest'

    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()
        self.prefix = app.config['API_PREFIX']
        self.pdf_path = os.path.join(os.path.dirname(__file__), 'sources/pdf_extract_test.pdf')
        self.references_path = os.path.join(os.path.dirname(__file__), 'sources/output_pdf_extract_test')
        self.pdf = open(self.pdf_path, 'rb')
        self.references = result
        self.url_base = 'http://0.0.0.0:5001'

    def test_base(self):
        if not self.app:
            raise AssertionError

    def test_pdf_extract(self):
        files = {}
        ret = requests.post(self.url_base + self.prefix + '/refs/pdf', files=files)
        if not ret:
            raise AssertionError
        jdata = ret.json()
        if not jdata:
            raise AssertionError
        token = jdata.get('job', None)
        if not token:
            raise AssertionError
        while done:
            references = (jdata.get('result') or {}).get('references', None)
            self.assertEqual(references, self.references)
            break
            time.sleep(10)

unittest.main()
