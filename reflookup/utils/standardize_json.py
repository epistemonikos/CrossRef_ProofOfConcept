from copy import deepcopy


class StandardDict:
    d = {
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

    def getEmpty(self):
        return deepcopy(self.d)


def crossref_to_standard(crossrefJson):
    standard = StandardDict().getEmpty()
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

    std = StandardDict().getEmpty()
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
