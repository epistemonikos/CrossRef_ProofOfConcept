import urllib.parse
from functools import reduce

import requests
from bs4 import BeautifulSoup
from flask_restful import abort

from reflookup import app
from reflookup.utils.standardize_json import scopus_to_standard
from reflookup.utils.standardize_json import standardize_pubmed_summary
import xml.etree.ElementTree as ET


def get_scopus_references(doi):
    params = {
        "apiKey": app.config["SCOPUS_API_KEY"]
    }
    headers = {
        "Accept": "text/xml"
    }
    resp = requests.get(app.config["SCOPUS_URI"] + doi, params=params,
                        headers=headers)

    if resp.status_code == 200:
        xml = ET.fromstring(resp.text)

        references = xml.findall("default:originalText//ce:bib-reference",
                                 app.config['SCOPUS_DTD'])

        refs = []
        for r in references:
            refs.append(scopus_to_standard(r))

        return refs

    elif resp.status_code == 404:
        abort(404, message='Resource not found.')
    else:
        abort(resp.status_code,
              message="Couldn't retrieve references for DOI:" + doi)


def getPubMedID(standardjson):
    if not standardjson['ids']['pubmed'] and standardjson['ids']['doi']:
        standardjson['ids']['pubmed'] = getPubMedIDByDoi(
            standardjson['ids']['doi'])
    return standardjson


def getSearchTerms(standardjson):
    searchterms = []
    # add title to the search
    if standardjson['title']:
        searchterms.append(standardjson['title'] + '[Title]')
    if standardjson['authors']:
        for author in standardjson['authors']:
            searchterms.append(author['family'] + '[Author]')
    term = reduce(lambda a, b: a + ' ' + b, searchterms, '')
    return term


def getPubMedIDByDoi(doi, VERIFY=True):
    soup = requestPubMed(doi)
    if soup and soup.idlist.find('id'):
        if VERIFY:
            if getDoi(soup.id.get_text()) == doi:
                return soup.id.get_text()
            else:
                return ''
        else:
            return soup.id.get_text()
    else:
        return ''


def searchInPubMed(terms):
    soup = requestPubMed(terms)
    if soup.find('idlist') and soup.idlist.find('id'):
        listOfID = soup.find_all('id')
        if (len(listOfID) == 1):
            return listOfID[0].get_text()
        else:
            return ''
    else:
        return ''


def getDoi(pubmedID):
    response = requests.get(
        'http://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=pubmed&rettype=abstract&id=' + pubmedID)
    cont = response.content.decode('utf8')
    soup = BeautifulSoup(cont, 'html.parser')
    if soup.find('item', {'name': 'doi'}):
        return soup.find('item', {'name': 'doi'}).get_text()


# Given a PubMedId return a list, with the the references on PubMed
def getRefID(pubmedID):
    response = requests.get(
        'http://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&rettype=pubmed_pubmed_refs&id=' + pubmedID)
    cont = response.content.decode('utf8')
    soup = BeautifulSoup(cont, 'html.parser')
    if soup.find('commentscorrectionslist'):
        ref_list = soup.find('commentscorrectionslist').find_all('pmid')
        return list(map(lambda x: x.get_text(), ref_list))
    else:
        return []


def requestPubMed(term):
    url = urllib.parse.quote_plus(term)
    response = requests.get(
        'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=' + url)
    return BeautifulSoup(response.content.decode('utf8'), 'html.parser')


def requestSummary(pubmedID):
    response = requests.get(
        'http://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=pubmed&rettype=abstract&id=' + pubmedID)
    return BeautifulSoup(response.content.decode('utf8'), 'html.parser')


def getReferenceInfo(listPMID):
    reference_list = []
    for id in listPMID:
        reference_list.append(standardize_pubmed_summary(requestSummary(id)))
    return reference_list
