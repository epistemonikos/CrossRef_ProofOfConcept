import reflookup
from reflookup.utils.parsers.wiley import WileyParser
from tests.unittests import parsertest
import json
import os


class WileyParserTest(parsertest.BaseParserTest):
    @classmethod
    def setUpClass(self):
        reflookup.app.config['TESTING'] = True
        self.url = "http://onlinelibrary.wiley.com/doi/10.1111/acel.12547/full"
        self.path = os.path.join(os.path.dirname(__file__), 'sources/wiley.json')
        with open(self.path, 'r') as result:
            self.data = json.load(result)
        self.parser = WileyParser()
        self.parser.parse(self.url)
