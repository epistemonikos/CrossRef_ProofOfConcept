import unittest
from unittest import TestCase
import reflookup
from reflookup.utils.parsers.bmc import BMCParser

class BMCParserTest(TestCase):

    def __init__(self):
        super().__init__()
        self.url = ""
        self.data = {}
        self.parser = BMCParser()
        self.parser.parse(self.url)

    def setUp(self):
        reflookup.app.config['TESTING'] = True
        self.app = reflookup.app.test_client()

    def test_parse_title(self):
        title = self.parser.get_title()
        self.assertEqual(title, self.data["title"])

    def test_parse_journal(self):
        journal = self.parser.get_journal()
        self.assertEqual(journal, self.data["publication_info"]["journal"])

    def test_parse_year(self):
        year = self.parser.get_year()
        self.assertEqual(year, self.data["publication_info"]["year"])

    def test_parse_volume(self):
        volume = self.parser.get_volume()
        self.assertEqual(volume, self.data["publication_info"]["volume"])

    def test_parse_issue(self):
        issue = self.parser.get_issue()
        self.assertEqual(issue, self.data["publication_info"]["issue"])

    def test_parse_pages(self):
        pages = self.parser.get_pages()
        self.assertEqual(pages, self.data["publication_info"]["pages"])

    def test_parse_citation(self):
        citation = self.parser.get_citation()
        self.assertEqual(citation, self.data["citation"])

    def test_parse_doi(self):
        doi = self.parser.get_doi()
        self.assertEqual(doi, self.data["ids"]["doi"])

    def test_parse_pubmedID(self):
        pmid = self.parser.get_pubmedID()
        self.assertEqual(pmid, self.data["ids"]["pmid"])

    def test_parse_authors(self):
        authors = self.parser.get_authors()
        self.assertEqual(authors, self.data["authors"])

    def test_parse_abstract(self):
        abstract = self.parser.get_abstract()
        self.assertEqual(abstract, self.data["abstract"])

    def test_parse_keywords(self):
        keywords = self.parser.get_keywords()
        self.assertEqual(keywords, self.data["keywords"])

    def test_parse_references(self):
        references = self.parser.get_references()
        self.assertEqual(references, self.data["references"])