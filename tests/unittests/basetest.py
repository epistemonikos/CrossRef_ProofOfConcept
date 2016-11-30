import unittest
from unittest import TestCase
import reflookup


class BaseTest(TestCase):
    """
    This is a base testing class for crossref and mendeley services.
    """
    def setUp(self):
        """
        This is an initial method to run the testing below and the testing in other class that inherit from this class
        """
        reflookup.app.config['TESTING'] = True
        self.app = reflookup.app.test_client()
        self.prefix = reflookup.app.config['API_PREFIX_V1']
        self.test_cite = 'Costello JT, Algar LA, Donnelly AE. Effects of wholebody cryotherapy (−110°C) on proprioception and indices of muscle damage. Scandinavian Journal of Medicine and Science in Sports'
        self.test_cite_mendeley = 'Nobili V, Parkes J, Bottazzo G, Marcellini M, Cross R, et al. (2009) Performance of ELF serum markers in predicting fibrosis stage in pediatric non-alcoholic fatty liver disease. Gastroenterology 136: 160–167. doi: 10.1053/j.gastro.2008.09.013'
        self.cr_doi = '10.1111/j.1600-0838.2011.01292.x'
        self.md_doi = '10.1053/j.gastro.2008.09.013'

    def test_base(self):
        """
        This is a simple test to makesure that the services is running
        """
        assert self.app


if __name__ == '__main__':
    unittest.main()
