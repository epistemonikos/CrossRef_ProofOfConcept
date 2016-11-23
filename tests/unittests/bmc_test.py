import unittest
import reflookup
from reflookup.utils.parsers.bmc import BMCParser
from tests.unittests import parsertest
import json
import os


class BMCParserTest(parsertest.BaseParserTest):

    def setUp(self):
        reflookup.app.config['TESTING'] = True
        self.url = "http://bmcnephrol.biomedcentral.com/articles/10.1186/s12882-016-0293-8"
        self.path = os.path.join(os.path.dirname(__file__), 'sources/bmc.json')
        with open(self.path, 'r') as result:
            self.data = json.load(result)
        self.parser = BMCParser()
        self.parser.parse(self.url)
