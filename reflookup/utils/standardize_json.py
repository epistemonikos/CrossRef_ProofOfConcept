from reflookup import app
from copy import deepcopy


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

    def getEmpty(self):
        return deepcopy(self.doc_dict)


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


def scopus_to_standard(xml):
    resp = StandardDict().getEmpty()

    coredata = xml.find('default:coredata', app.config['SCOPUS_DTD'])

    # Title
    title = coredata.find('dc:title', app.config['SCOPUS_DTD'])
    resp['title'] = title.text.strip()

    # Abstract
    abstract = coredata.find('dc:description', app.config['SCOPUS_DTD'])
    resp['abstract'] = abstract.text.strip()

    # Type
    type = coredata.find('default:pubType', app.config['SCOPUS_DTD'])
    access = coredata.find('default:openaccessArticle',
                           app.config['SCOPUS_DTD'])
    if access.text.strip() == 'false':
        resp['type'] = type.text.strip() + ' (Closed Access)'
    else:
        resp['type'] = type.text.strip() + ' (Open Access)'

    # IDs
    doi = coredata.find('prism:doi', app.config['SCOPUS_DTD'])
    resp['ids']['doi'] = doi.text.strip()

    scopus_id = xml.find('default:scopus-id', app.config['SCOPUS_DTD'])
    resp['ids']['scopus'] = int(scopus_id.text.strip())

    # Publication Info
    journal = coredata.find('prism:publicationName', app.config['SCOPUS_DTD'])
    resp['publication_type']['title'] = journal.text.strip()

    volume = coredata.find('prism:volume', app.config['SCOPUS_DTD'])
    resp['publication_type']['volume'] = int(volume.text.strip())

    year = coredata.find('prism:coverDisplayDate', app.config['SCOPUS_DTD'])
    resp['publication_type']['year'] = int(year.text.strip()[-4:])

    issue = coredata.find('prism:issueIdentifier', app.config['SCOPUS_DTD'])
    resp['publication_type']['issue'] = int(issue.text.strip())

    issn = coredata.find('prism:issn', app.config['SCOPUS_DTD'])
    resp['publication_type']['issn'] = int(issn.text.strip())

    first_page = coredata.find('prism:startingPage', app.config['SCOPUS_DTD'])
    last_page = coredata.find('prism:endingPage', app.config['SCOPUS_DTD'])
    resp['publication_type']['pagination'] = {
        'first': first_page.text.strip(),
    # La numeracion incluye letras, no se pueden
        'last': last_page.text.strip()  # guardar como int
    }

    # Authors
    resp['authors'] = [x.text.strip() for x in coredata.findall('dc:creator',
                                                                app.config[
                                                                    'SCOPUS_DTD'])]

    # References
    references = xml.findall('default:originalText//ce:bib-reference',
                             app.config['SCOPUS_DTD'])
    resp['references'] = [scopus_ref_to_standard(r) for r in references]

    resp['source'] = 'Scopus API'
    return resp


def scopus_ref_to_standard(r):
    ref_dict = StandardDict().getEmpty()
    ref_text = ''
    for a in r.findall('.//sb:author', app.config['SCOPUS_DTD']):
        a_dict = {'family': a.find('ce:surname',
                                   app.config['SCOPUS_DTD']).text,
                  'given': a.find('ce:given-name',
                                  app.config['SCOPUS_DTD']).text}
        ref_text += a_dict['family'] + ' ' + a_dict['given'] + ', '
        ref_dict['authors'].append(a_dict)
    ref_text = ref_text[:-2]

    host = r.find('.//sb:host', app.config['SCOPUS_DTD'])
    other_ref = r.find('ce:other-ref', app.config['SCOPUS_DTD'])
    if host:
        # Reference split in authors and publication info.
        date = host.find('sb:issue/sb:date', app.config['SCOPUS_DTD']).text
        if date:
            ref_dict['publication_type']['year'] = int(date)
            ref_text += ' ({}).'.format(date)
        else:
            ref_text += '.'

        title = host.find('.//sb:maintitle', app.config['SCOPUS_DTD']).text
        if title:
            ref_dict['publication_type']['title'] = title
            ref_text += ' ' + title

        volume = host.find('sb:issue/sb:series/sb:volume-nr',
                           app.config['SCOPUS_DTD']).text
        pages = host.find('sb:pages', app.config['SCOPUS_DTD'])
        if volume:
            ref_dict['publication_type']['volume'] = int(volume)
            if title:
                ref_text += ', ' + volume
        if pages:
            first = int(
                pages.find('sb:first-page', app.config['SCOPUS_DTD']).text)
            last = int(
                pages.find('sb:last-page', app.config['SCOPUS_DTD']).text)
            ref_dict['publication_type']['pages'] = {
                'first': first,
                'last': last
            }
            if title:
                ref_text += ', {}-{}'.format(first, last)
        ref_dict['publication_type']['reference'] = ref_text
    if other_ref:
        # Reference in plain text.
        ref_dict['publication_type']['reference'] = other_ref.find(
            'ce:textref', app.config['SCOPUS_DTD']).text

    return ref_dict


def standardize_pubmed_summary(xml):
    parsedSummany = StandardDict().getEmpty()

    if xml.find('item', {'name': 'Title'}).get_text() != '':
        parsedSummany['title'] = xml.find('item', {'name': 'Title'}).get_text()

    if xml.find('item', {'name': 'PubDate'}).get_text() != '':
        parsedSummany['publication_type']['year'] = xml.find('item', {
            'name': 'PubDate'}).get_text()

    if xml.find('item', {'name': 'FullJournalName'}).get_text() != '':
        parsedSummany['publication_type']['title'] = xml.find('item', {
            'name': 'FullJournalName'}).get_text()

    if xml.find('item', {'name': 'AuthorList'}).get_text() != '':
        authorList = []
        for author in xml.find('item', {'name': 'AuthorList'}).find_all('item',
                                                                        {
                                                                            'name': 'Author'}):
            authorList.append(author.get_text())
        parsedSummany['authors'] = authorList

    if (xml.find('item', {'name': 'doi'}) and xml.find('item', {
        'name': 'doi'}).get_text() != ''):
        parsedSummany['ids']['doi'] = xml.find('item',
                                               {'name': 'doi'}).get_text()

    if xml.find('item', {'name': 'pubmed'}).get_text() != '':
        parsedSummany['ids']['pubmed'] = xml.find('item', {
            'name': 'pubmed'}).get_text()

    if xml.find('item', {'name': 'Issue'}).get_text() != '':
        parsedSummany['publication_type']['issue'] = xml.find('item', {
            'name': 'Issue'}).get_text()

    if xml.find('item', {'name': 'ISSN'}).get_text() != '':
        parsedSummany['publication_type']['ISSN'] = xml.find('item', {
            'name': 'ISSN'}).get_text()

    if xml.find('item', {'name': 'PubType'}).get_text() != '':
        parsedSummany['publication_type']['type'] = xml.find('item', {
            'name': 'PubType'}).get_text()

    if xml.find('item', {'name': 'Volume'}).get_text() != '':
        parsedSummany['publication_type']['volume'] = xml.find('item', {
            'name': 'Volume'}).get_text()

    if xml.find('item', {'name': 'Lang'}).get_text() != '':
        parsedSummany['language'] = xml.find('item',
                                             {'name': 'Lang'}).get_text()
    return parsedSummany
