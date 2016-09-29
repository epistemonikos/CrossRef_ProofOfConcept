__map_crTypes_RIS = {
    'book-section': 'CHAP',
    'monograph': None,
    'report': 'RPRT',
    'book-track': None,
    'journal-article': 'JOUR',
    'preprint': None,
    'book-part': 'CHAP',
    'other': 'GEN',
    'book': 'BOOK',
    'journal-volume': 'JOUR',
    'reference-entry': None,
    'book-set': None,
    'proceedings-article': 'CPAPER',
    'journal': 'JFULL',
    'component': None,
    'book-chapter': 'CHAP',
    'report-series': 'SER',
    'proceedings': 'CONF',
    'standard': 'STAND',
    'reference-book': 'BOOK',
    'journal-issue': 'JFULL',
    'dissertation': None,
    'dataset': 'DATA',
    'book-series': 'SER',
    'edited-book': 'EDBOOK',
    'standard-series': 'SER'
}


class RISTypeException(Exception):
    def __init__(self, message):
        super().__init__()
        self.message = 'No matching RIS type found for ' + message


def dict2ris(in_data):

    """
    Parses a dict of bibliographic information and returns a string containing
    said information in RIS standard format.
    :param in_data: Python dictionary containing bibliographic information.
    :return: Python string containing the bibliographic information in RIS
    format.
    """

    o_type = in_data.get('type')
    ris_type = __map_crTypes_RIS.get(o_type, None)
    if not ris_type:
        raise RISTypeException(o_type)

    ris_header = 'TY  - {ty}\n'.format(ty=ris_type)
    ris_body = ''
    ris_end = 'ER  - \n'

    for k, v in in_data.items():
        if k == 'DOI':
            ris_body += 'DOI  - {doi}\n'.format(doi=v)
        elif k == 'ISSN':
            ris_body += 'SN  - {issn}\n'.format(issn=v)
        elif k == 'URL':
            ris_body += 'UR  - {url}\n'.format(url=v)
        elif k == 'author':
            if type(in_data[k]) == list:
                for author in in_data[k]:
                    name = '{ln}, {fn}'.format(ln=author['family'],
                                               fn=author['given'])
                    ris_body += 'AU  - {au}\n'.format(au=name)
            else:
                name = '{ln}, {fn}'.format(ln=v['family'],
                                           fn=v['given'])
                ris_body += 'AU  - {au}\n'.format(au=name)
        elif k == 'container-title':
            javb = v[0]
            jfull = v[1]

            ris_body += 'JA  - {ja}\nJF  - {jf}\n'.format(ja=javb, jf=jfull)

        ris_final = '{head}{body}{end}'.format(head=ris_header,
                                               body=ris_body,
                                               end=ris_end)

        return ris_final
