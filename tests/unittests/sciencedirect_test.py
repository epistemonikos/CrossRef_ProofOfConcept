import reflookup
from reflookup.utils.parsers.sciencedirect import ScienceDirectParser
from tests.unittests import parsertest
import json
import os


class ScienceDirectParserTest(parsertest.BaseParserTest):

    def setUpClass(self):
        reflookup.app.config['TESTING'] = True
        # TODO: bucar una URL para testear ScienceDirect + output esperado
        self.url = "http://www.google.cl/"
        self.path = os.path.join(os.path.dirname(__file__), 'sources/sciencedirect.json')
        with open(self.path, 'r') as result:
            self.data = json.load(result)
        self.parser = ScienceDirectParser()
        self.parser.parse(self.url)
