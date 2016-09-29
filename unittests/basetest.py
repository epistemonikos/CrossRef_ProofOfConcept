import unittest
from unittest import TestCase
import reflookup


class BaseTest(TestCase):
    def setUp(self):
        reflookup.app.config['TESTING'] = True
        self.app = reflookup.app.test_client()
        self.prefix = reflookup.app.config['API_PREFIX']
        self.test_cite = 'Costello 2012 {published data only} Costello J. Personal communication March 2014. ∗ Costello JT, Algar LA, Donnelly AE. Effects of wholebody cryotherapy (−110°C) on proprioception and indices of muscle damage. Scandinavian Journal of Medicine and Science in Sports 2012;22(2):190–8. [DOI: 10.1111/ j.1600-0838.2011.01292.x]'

    def test_base(self):
        assert self.app


if __name__ == '__main__':
    unittest.main()
