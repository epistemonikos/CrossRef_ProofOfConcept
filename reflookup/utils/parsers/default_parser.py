from bs4 import BeautifulSoup
import urllib.request

class DefaultParser():

    def parse(self, url):
        html = urllib.request.urlopen(url).read()
        self.soup = BeautifulSoup(html, 'html.parser')
        return {
            'title': self.get_title(),
            'publication_info': self.get_publication_info(),
            'citation': self.get_citation(),
            'ids': self.get_identifiers(),
            'authors': self.get_authors(),
            'abstract': self.get_abstract(),
            'keywords': self.get_keywords(),
            'references': self.get_references()
        }

    def get_title(self):
        title  = self.soup.find('meta', attrs={"name": 'DC.title'})
        if not title:
            title = self.soup.find('meta', attrs={"name": 'citation_title'})
        if title:
            title = title["content"]
        return title

    def get_publication_info(self):
        """
            this function get publication information from html.
            :params soup: instance of BeautifulSoup class
        """
        return {
            'journal': self.get_journal(),
            'year': self.get_year(),
            'volume': self.get_volume(),
            'issue': self.get_issue(),
            'pages': self.get_pages()
        }

    def get_journal(self):
        journal = self.soup.find('meta', attrs={"name": 'citation_journal_title'})
        if journal:
            journal = journal["content"]
        return journal

    def get_year(self):
        year = self.soup.find('meta', attrs={"name": 'citation_publication_date'})
        if year:
            year = year["content"].split('/')[0]
        if not year:
            year = self.soup.find('meta', attrs={"name": 'DC.Date'})
            if year:
                year = year["content"].split('-')[0]
        return year

    def get_volume(self):
        volume = self.soup.find('meta', attrs={"name": 'citation_volume'})
        if volume:
            volume = volume["content"]
        return volume

    def get_issue(self):
        issue = self.soup.find('meta', attrs={"name": 'citation_issue'})
        if issue:
            issue = issue["content"]
        return issue

    def get_pages(self):
        first = self.soup.find('meta', attrs={"name": 'citation_firstpage'})
        last = self.soup.find('meta', attrs={"name": 'citation_lastpage'})
        return {
            'first': first["content"] if first else None,
            'last': last["content"] if last else None
        }

    def get_citation(self):
        return None

    def get_identifiers(self):
        """
            this function get identifiers from html.
            :params soup: instance of BeautifulSoup class
        """
        return {
            'doi': self.get_doi(),
            'pmid': self.get_pubmedID()
        }

    def get_doi(self):
        doi = self.soup.find('meta', attrs={"name": 'citation_doi'})
        if doi:
            doi = doi["content"]
        if not doi:
            doi = self.soup.find('meta', attrs={"name": 'DC.Identifier'})
            if doi:
                doi = doi["content"]
        return doi

    def get_pubmedID(self):
        pmid = self.soup.find('meta', attrs={"name": 'citation_pmid'})
        if pmid:
            pmid = pmid["content"]
        return pmid

    def get_authors(self):
        """
            this function get authors from html.
            :params soup: instance of BeautifulSoup class
        """
        authors = self.soup.find_all('meta', attrs={"name": 'citation_author'})
        return [a["content"] for a in authors]

    def get_abstract(self):
        """
            this function get abstract from html.
            :params soup: instance of BeautifulSoup class
        """
        abstract = self.soup.find('meta', attrs={"name": 'DC.Description'})
        if abstract:
            abstract = abstract["content"]
        return abstract

    def get_keywords(self):
        """
            this function get keywords from html.
            :params soup: instance of BeautifulSoup class
        """
        return []

    def get_references(self):
        """
        this function get all references from html.
        :params soup: instance of BeautifulSoup class
        """
        refs = self.soup.findAll('meta', attrs={"name": 'citation_reference'})
        resp = []
        for r in refs:
            dic = {}
            authors = []
            for p in r['content'][9:].split(';citation_'):
                [k, v] = p.split('=')
                if k == "author":
                    authors.append(v)
                else:
                    dic[k] = v
            dic["authors"] = authors
            resp.append(dic)
        return [self.get_reference_info(r) for r in resp]

    def get_reference_info(self, ref):
        return {
            'authors': self.get_ref_authors(ref),
            'year': self.get_ref_year(ref),
            'title': self.get_ref_title(ref),
            'journal': self.get_ref_journal(ref),
            'volume': self.get_ref_volume(ref),
            'pages': self.get_ref_pages(ref),
            'reference': self.get_ref_text(ref),
            'ids': self.get_ref_identifiers(ref)
        }

    def get_ref_authors(self, ref):
        if isinstance(ref, dict):
            authors = ref.get("authors", [])
            return [a.strip() for a in authors]
        return None

    def get_ref_year(self, ref):
        if isinstance(ref, dict):
            return ref.get("citation_year", None)
        return None

    def get_ref_title(self, ref):
        if isinstance(ref, dict):
            return ref.get("citation_title", None)
        return None

    def get_ref_journal(self, ref):
        if isinstance(ref, dict):
            return ref.get("citation_journal_title", None)
        return None

    def get_ref_volume(self, ref):
        if isinstance(ref, dict):
            return ref.get("citation_volume", None)
        return None

    def get_ref_pages(self, ref):
        if isinstance(ref, dict):
            pages = ref.get("citation_pages", None)
            if pages:
                pages = pages.split('-')
                return {
                    "first": pages[0],
                    "last": pages[1]
                }
        return None

    def get_ref_text(self, ref):
        return None

    def get_ref_identifiers(self, ref):
        return {
            'doi': self.get_ref_doi(ref),
            'pmid': self.get_ref_pubmedID(ref),
            'scholar': self.get_ref_scholar(ref)
        }

    def get_ref_doi(self, ref):
        if isinstance(ref, dict):
            return ref.get("citation_doi", None)
        return None

    def get_ref_pubmedID(self, ref):
        if isinstance(ref, dict):
            return ref.get("citation_pmid", None)
        return None

    def get_ref_scholar(self, ref):
        return None
