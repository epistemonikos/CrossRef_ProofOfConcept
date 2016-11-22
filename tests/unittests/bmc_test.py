import unittest
from unittest import TestCase
import reflookup
from reflookup.utils.parsers.bmc import BMCParser
import json
import os

class BMCParserTest(TestCase):

    def setUp(self):
        reflookup.app.config['TESTING'] = True
        self.url = "http://bmcnephrol.biomedcentral.com/articles/10.1186/s12882-016-0293-8"
        self.path = os.path.join(os.path.dirname(__file__), 'sources/bmc.json')
        with open(self.path, 'r') as result:
            self.data = json.load(result)
        self.parser = BMCParser()
        self.parser.parse(self.url)

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
        refs = self.parser.soup.body.find_all('cite', 'CitationContent')
        for i in range(0, len(refs)):
            with self.subTest(i=i):
                self.assertEqual(self.parser.get_ref_text(refs[i]), self.data["references"][i]["reference"])
                self.assertEqual(self.parser.get_ref_doi(refs[i]), self.data["references"][i]["ids"]["doi"])
                self.assertEqual(self.parser.get_ref_pubmedID(refs[i]), self.data["references"][i]["ids"]["pmid"])
                self.assertEqual(self.parser.get_ref_scholar(refs[i]), self.data["references"][i]["ids"]["scholar"])
