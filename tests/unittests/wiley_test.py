import reflookup
from reflookup.utils.parsers.wiley import WileyParser
from tests.unittests import parsertest
import json
import os


class WileyParserTest(parsertest.BaseParserTest):

    def setUp(self):
        reflookup.app.config['TESTING'] = True
        # TODO: bucar una URL para testear wiley + output esperado
        self.url = "http://www.google.cl/"
        self.path = os.path.join(os.path.dirname(__file__), 'sources/bmc.json')
        with open(self.path, 'r') as result:
            self.data = json.load(result)
        self.parser = WileyParser()
        self.parser.parse(self.url)
