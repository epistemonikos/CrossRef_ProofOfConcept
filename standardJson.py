__author__ = 'fmosso'
import json


def crossRefToStandard(crossrefJson):
    standard = {}
    title = crossrefJson.get('title', [''])
    standard['title'] = title[0] if len(title) > 0 else ''
    standard['type'] = crossrefJson.get('type', '')
    standard['abstract'] = ''
    standard['language'] = ''
    standard['ids'] = {}
    standard['ids']['doi'] = crossrefJson.get('DOI', '')
    standard['ids']['embase'] = ''
    standard['ids']['pubmed'] = ''
    standard['publication_type'] = {}
    standard['publication_type']['pagination'] = crossrefJson.get('page', '')
    standard['publication_type']['cited_medium'] = ''

    title_of_pub = crossrefJson.get('container-title', [''])
    standard['publication_type']['title'] = title_of_pub[0] if len(
        title_of_pub) > 0 else ''

    issn = crossrefJson.get('ISSN', '')
    standard['publication_type']['ISSN'] = issn[0] if len(issn) > 0 else ''
    standard['publication_type']['volume'] = crossrefJson.get('volume', '')

    issued_date = crossrefJson.get('issued', {'date-parts': [0]})
    standard['publication_type']['year'] = issued_date.get('date-parts',
                                                           [0])[0]

    standard['publication_type']['issue'] = crossrefJson.get('issue', '')
    standard['authors'] = []
    for author in crossrefJson.get('author', []):
        names = {'given': author.get('given', ''),
                 'family': author.get('family', '')}
        standard['authors'].append(names)
    return json.dumps(standard)
