import unittest

from tests.unittests.crossreftest import CrossRefTest
from tests.unittests.lookuptest import LookupTest
from tests.unittests.mendeleytest import MendeleyTest
from tests.unittests.pdf_extract_test import PdfExtractTest

from tests.unittests.parsertest import BaseParserTest
from tests.unittests.bmc_test import BMCParserTest
from tests.unittests.springer_test import SpringerParserTest
from tests.unittests.wiley_test import WileyParserTest

if __name__ == '__main__':
    unittest.main()
