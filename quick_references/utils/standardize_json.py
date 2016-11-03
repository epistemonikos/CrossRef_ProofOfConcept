from copy import deepcopy
from quick_references import app
import json
import xml.etree.ElementTree as ET

class StandardDict:
    d = {
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

    def getEmpty(self):
        return deepcopy(self.d)

def scopus_to_standard(resp):
    xml = ET.fromstring(resp)
    # xml = ET.parse("example/ex1.xml").getroot()

    references = xml.findall("default:originalText//ce:bib-reference", app.config['SCOPUS_DTD'])
    ref_json = []
    for r in references:
        ref_dict = StandardDict().getEmpty()
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

        ref_json.append(ref_dict)

    return ref_json

