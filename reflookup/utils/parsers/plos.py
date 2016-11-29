from reflookup.utils.parsers.default_parser import DefaultParser
import re


def trim_string(word):
    s = re.sub('\s+', ' ', word)
    s = re.sub(u"\u2013", "-", s)
    return s.strip()


class PlosParser(DefaultParser):

    def get_keywords(self):
        keywords = self.soup.find_all(attrs={"name": "keywords"})
        if keywords:
            keywords = trim_string(keywords[0]['content']).split(',')
            keywords = [trim_string(r) for r in keywords]
        return keywords

    def get_title(self):
        title = self.soup.body.find_all('div', 'title-authors')
        if title:
            title = trim_string(title[0].h1.text)
        return title

    def get_abstract(self):
        abstract = self.soup.body.find_all('div', 'abstract')
        if abstract:
            abstract = trim_string(abstract[0].p.text)
        return abstract

    def get_authors(self):
        authors_info = self.soup.body.find_all('a', 'author-name')
        authors = []
        for a in authors_info:
            authors.append(re.sub(',$', '', trim_string(a.text)))
        return authors

    def get_citation(self):
        cita = self.soup.body.find_all('div', 'articleinfo')
        if cita:
            cita = trim_string(cita[0].p.text)
            cita = re.sub('Citation:', '', cita)
        return cita

    def get_identifiers(self):
        return {
            'doi': self.get_doi(),
            'pmid': self.get_pubmedID(),
            'url': self.get_url()
        }

    def get_url(self):
        url = self.soup.find_all(attrs={"name": "citation_pdf_url"})
        if url:
            url = trim_string(url[0]['content'])
        return url

    def get_doi(self):
        doi = self.soup.body.find_all('li', id='artDoi')[0]
        if doi:
            doi = re.sub('.*doi.org/', '', trim_string(doi.text))
        return doi

    def get_issn(self):
        issn = self.soup.find_all(attrs={"name": "citation_issn"})
        if issn:
            issn = trim_string(issn[0]['content'])
        return issn

    def get_publication_info(self):
        return {
            'journal': self.get_journal(),
            'year': self.get_year(),
            'volume': self.get_volume(),
            'issue': self.get_issue(),
            'pages': self.get_pages(),
            'issn': self.get_issn()
        }

    def get_journal(self):
        journal = self.soup.body.find_all('h1', 'logo')
        if journal:
            journal = trim_string(journal[0].a.text)
        return journal

    def get_year(self):
        year = self.soup.find_all(attrs={"name": "citation_date"})
        if year:
            year = trim_string(year[0]['content'])
            year = re.search('\d{4}', year).group(0)
        return year

    def get_volume(self):
        volume = self.soup.find_all(attrs={"name": "citation_volume"})
        if volume:
            volume = trim_string(volume[0]['content'])
        return volume

    def get_issue(self):
        issue = self.soup.find_all(attrs={"name": "citation_issue"})
        if issue:
            issue = trim_string(issue[0]['content'])
        return issue

    def get_pages(self):
        page = self.soup.find_all(attrs={"name": "citation_firstpage"})
        if page:
            page = trim_string(page[0]['content'])
        return page

    def get_references(self):
        references = self.soup.body.find_all('ol', 'references')
        if references:
            references = references[0].contents
            references = [self.get_reference_info(r) for r in references]
        return references

    def get_ref_text(self, ref):
        text = re.sub(u"\u2013", "-", ref.text)
        lista = text.split('\n')
        lista.pop(0)
        return trim_string(' '.join(lista[:-6]))