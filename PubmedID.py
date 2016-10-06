import time

__author__ = 'fmosso'
import requests
import urllib
from bs4 import BeautifulSoup
import json
from functools import reduce

def getPubMedID (standardjson):
    if not standardjson['ids']['pubmed']:
        if standardjson['ids']['doi']:
            standardjson['ids']['pubmed'] = (getPubMedIDByDoi(standardjson['ids']['doi']))
        #else:
            #standardjson['ids']['pubmed'] = searchInPubMed(getSearchTerms(standardjson))
    return json.dumps(standardjson)


def getSearchTerms(standardjson):
    searchterms = []
    #add title to the search
    if standardjson['title']:
        searchterms.append(standardjson['title']+'[Title]')
    if standardjson['authors']:
        for author in standardjson['authors']:
            searchterms.append(author['family']+'[Author]')
    term = reduce(lambda a,b: a+" "+b, searchterms, "")
    return term


def getPubMedIDByDoi(doi,VERIFY = True):
    soup = requestPubMed(doi)
    if soup and soup.idlist.find('id'):
        if VERIFY:
            if getDoi(soup.id.get_text()) == doi:
                return soup.id.get_text()
            else:
                return ""
        else:
            return soup.id.get_text()
    else:
        return ""

def searchInPubMed(terms):
    soup = requestPubMed(terms)
    if soup.find('idlist') and soup.idlist.find('id'):
        listOfID = soup.find_all('id')
        if (len(listOfID) == 1):
            return listOfID[0].get_text()
        else:
            return ""
    else:
        return ""


def getDoi(pubmedID):
    response = requests.get("http://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=pubmed&rettype=abstract&id="+pubmedID)
    cont = response.content.decode('utf8')
    soup = BeautifulSoup(cont, 'html.parser')
    if soup.find('item', {'name' :'doi'}):
        return soup.find('item', {'name' :'doi'}).get_text()

#Given a PubMedId return a list, withe the references on PubMed
#def getRefID(pubmedID):
#    response = requests.get("http://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&rettype=pubmed_pubmed_refs&id="+pubmedID)
#    cont = response.content.decode('utf8')
#    soup = BeautifulSoup(cont, 'html.parser')
#    if soup.find('commentscorrectionslist'):
#        ref_list = soup.find('commentscorrectionslist').find_all('pmid')
#        return list(map(lambda x: x.get_text(),ref_list ))
#    else:
#        return []

def requestPubMed(term):
    url = urllib.parse.quote_plus(term)
    response = requests.get("https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=" + url)
    return BeautifulSoup(response.content.decode('utf8'), 'html.parser')

def requestSummary(pubmedID):
    response = requests.get("http://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=pubmed&rettype=abstract&id="+pubmedID)
    return BeautifulSoup(response.content.decode('utf8'), 'html.parser')

#extracts the relevant information from the summary
def parseSummary(xml):
    parsedSummany = {}
    if xml.find('item', {'name' :'Title'}):
        parsedSummany['Title'] = xml.find('item', {'name' :'Title'}).get_text()
    if xml.find('item', {'name' :'PubDate'}):
        parsedSummany['Date'] = xml.find('item', {'name' :'PubDate'}).get_text()
    if xml.find('item', {'name' :'EPubDate'}):
        parsedSummany['EDate'] = xml.find('item', {'name' :'EPubDate'}).get_text()
    if xml.find('item', {'name' :'Source'}):
        parsedSummany['Journal'] = xml.find('item', {'name' :'Source'}).get_text()
    if xml.find('item', {'name' :'AuthorList'}):
        authorList = []
        for author in xml.find('item', {'name' :'AuthorList'}).find_all('item', {'name' :'Author'}):
            authorList.append(author.get_text())
        parsedSummany['Authors'] = authorList
    return json.dumps(parsedSummany)


#print(getPubMedIDByDoi("10.1371/journal.pbio.0000005"))
#print(getPubMedIDByDoi("10.1093/nar/gks1195"))
#print(getPubMedIDByDoi("erveirvkml"))
#print(getPubMedIDByDoi("10.1016/j.bbmt.2016.05.123")) #wrong DOI

#print(searchInPubMed("Monitoring the chromosome Zhou Y"))
#print(requestSummary("27706929"))


#print (searchInPubMed(getSearchTerms(0)))

#print (urllib.parse.quote_plus("Patterns of gene-specific and total transcriptional activity during the Plasmodium falciparum intraerythrocytic developmental cycle."))
