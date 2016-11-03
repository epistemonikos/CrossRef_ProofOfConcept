from reflookup import app
from copy import deepcopy
import xml.etree.ElementTree as ET

class StandardDict:
    doc_dict = {
        'title': None,
        'abstract': None,
        'language': None,
        'type': None,
        'ids': {
            'doi': None,
            'embase': None,
            'pubmed': None,
            'scopus': None
        },
        'publication_type': {
            'pagination': None,
            'cited_medium': None,
            'title': None,
            'issn': None,
            'volume': None,
            'year': None,
            'issue': None
        },
        'authors': [
            # {
            #     'given': None,
            #     'family': None
            # }
        ],
        'source': None
    }

    ref_dict = {
        'reference': None,
        'publication_type': {
            'pagination': {
                'first': None,
                'Last': None
            },
            'title': None,
            'issn': None,
            'volume': None,
            'year': None,
            'issue': None
        },
        'authors': [
            # {
            #     'given': None,
            #     'family': None
            # }
        ],
        'source': None
    }

    def getEmptyDoc(self):
        return deepcopy(self.doc_dict)

    def getEmptyRef(self):
        return deepcopy(self.ref_dict)


def crossref_to_standard(crossrefJson):
    standard = StandardDict().getEmptyDoc()
    standard['source'] = 'CrossRef'

    title = crossrefJson.get('title', [None])
    standard['title'] = title[0] if len(title) > 0 else None
    standard['type'] = crossrefJson.get('type', None)
    standard['ids']['doi'] = crossrefJson.get('DOI', None)
    standard['publication_type']['pagination'] = crossrefJson.get('page', None)

    title_of_pub = crossrefJson.get('container-title', [None])
    standard['publication_type']['title'] = title_of_pub[0] if len(
        title_of_pub) > 0 else None

    issn = crossrefJson.get('ISSN', [None])
    standard['publication_type']['issn'] = issn[0] if len(issn) > 0 else None
    standard['publication_type']['volume'] = crossrefJson.get('volume', None)

    issued_date = crossrefJson.get('issued', {'date-parts': [0]})
    standard['publication_type']['year'] = issued_date.get('date-parts',
                                                           [0])[0][0]

    standard['publication_type']['issue'] = crossrefJson.get('issue', None)
    for author in crossrefJson.get('author', []):
        names = {'given': author.get('given', None),
                 'family': author.get('family', None)}
        standard['authors'].append(names)

    return standard


def mendeley_to_standard(mjson):
    """
    Standardizes the Mendeley return JSON into our own format.
    :param mjson: The Mendeley return JSON in dict format.
    :return: An Epistemonikos standard JSON in dict format.
    """

    std = StandardDict().getEmptyDoc()
    std['source'] = 'Mendeley'
    std['type'] = mjson['type']

    std['title'] = mjson['title']
    std['abstract'] = mjson['abstract']

    ids = mjson.get('identifiers')
    if ids:
        std['ids']['doi'] = ids.get('doi', None)
        std['ids']['pubmed'] = ids.get('pmid', None)
        std['ids']['scopus'] = ids.get('scopus', None)

    std['publication_type']['title'] = mjson['source']
    std['publication_type']['year'] = int(mjson['year'])

    if ids:
        std['publication_type']['issn'] = ids.get('issn', None)

    for a in mjson['authors']:
        std['authors'].append({
            'given': a.get('first_name', None),
            'family': a.get('last_name', None)
        })

    return std


def scopus_to_standard(scopusXML, doi):
    xml = ET.fromstring(scopusXML)

    references = xml.findall("default:originalText//ce:bib-reference", app.config['SCOPUS_DTD'])
    ref_json = {
        'doi': doi,
        'references': []
    }

    for r in references:
        ref_dict = StandardDict().getEmptyRef()
        ref_text = ""
        for a in r.findall(".//sb:author", app.config['SCOPUS_DTD']):
            a_dict = {}
            a_dict["family"] = a.find("ce:surname", app.config['SCOPUS_DTD']).text
            a_dict["given"] = a.find("ce:given-name", app.config['SCOPUS_DTD']).text
            ref_text += a_dict["family"] + " " + a_dict["given"] + ", "
            ref_dict["authors"].append(a_dict)
        ref_text = ref_text[:-2]

        host = r.find(".//sb:host", app.config['SCOPUS_DTD'])
        other_ref = r.find("ce:other-ref", app.config['SCOPUS_DTD'])
        if host:
            # Reference split in authors and publication info.
            date = host.find("sb:issue/sb:date", app.config['SCOPUS_DTD']).text
            if date:
                ref_dict['publication_type']['year'] = int(date)
                ref_text += " ({}).".format(date)
            else:
                ref_text += "."

            title = host.find(".//sb:maintitle", app.config['SCOPUS_DTD']).text
            if title:
                ref_dict['publication_type']['title'] = title
                ref_text += " " + title

            volume = host.find("sb:issue/sb:series/sb:volume-nr", app.config['SCOPUS_DTD']).text
            pages = host.find("sb:pages", app.config['SCOPUS_DTD'])
            if volume:
                ref_dict['publication_type']['volume'] = int(volume)
                if title:
                    ref_text += ", " + volume
            if pages:
                first = int(pages.find("sb:first-page", app.config['SCOPUS_DTD']).text)
                last = int(pages.find("sb:last-page", app.config['SCOPUS_DTD']).text)
                ref_dict['publication_type']['pages'] = {
                    'first': first,
                    'last': last
                }
                if title:
                    ref_text += ", {}-{}".format(first, last)
            ref_dict['publication_type']['reference'] = ref_text
        if other_ref:
            # Reference in plain text.
            ref_dict['publication_type']['reference'] = other_ref.find("ce:textref", app.config['SCOPUS_DTD']).text

        ref_json['references'].append(ref_dict)

    return ref_json
