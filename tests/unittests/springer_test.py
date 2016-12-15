import reflookup
from reflookup.utils.parsers.springer import SpringerParser
from tests.unittests import parsertest
import json
import os


class SpringerParserTest(parsertest.BaseParserTest):

    def setUpClass(self):
        reflookup.app.config['TESTING'] = True
        self.url = "http://link.springer.com/article/10.1007%2Fs12032-015-0718-4"
        self.path = os.path.join(os.path.dirname(__file__), 'sources/springer.json')
        with open(self.path, 'r') as result:
            self.data = json.load(result)
        self.parser = SpringerParser()
        self.parser.parse(self.url)
