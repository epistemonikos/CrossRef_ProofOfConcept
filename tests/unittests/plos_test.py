import reflookup
from reflookup.utils.parsers.plos import PlosParser
from tests.unittests import parsertest
import json
import os


class PlosParserTest(parsertest.BaseParserTest):
    @classmethod
    def setUpClass(self):
        reflookup.app.config['TESTING'] = True
        self.url = "http://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.0030208"
        self.path = os.path.join(os.path.dirname(__file__), 'sources/plos.json')
        with open(self.path, 'r') as result:
            self.data = json.load(result)
        self.parser = PlosParser()
        self.parser.parse(self.url)
