import json

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

    def __repr__(self):
        return self.message

    def __str__(self):
        return self.message


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
            for issn in v:
                ris_body += 'SN  - {issn}\n'.format(issn=issn)

        elif k == 'URL':
            ris_body += 'UR  - {url}\n'.format(url=v)

        elif k == 'author':
            for author in in_data[k]:
                name = '{ln}, {fn}'.format(ln=author['family'],
                                           fn=author['given'])
                ris_body += 'AU  - {au}\n'.format(au=name)

        elif k == 'container-title':
            for title in v:
                ris_body += 'JF  - {jf}\n'.format(jf=title)

        elif k == 'short-container-title':
            for title in v:
                ris_body += 'JO  - {jo}\n'.format(jo=title)

        elif k == 'publisher':
            ris_body += 'PB  - {pb}\n'.format(pb=v)

        elif k == 'short-title':
            for title in v:
                ris_body += 'ST  - {st}\n'.format(st=title)

        elif k == 'title':
            for title in v:
                ris_body += 'TI  - {st}\n'.format(st=title)

        elif k == 'subtitle':
            for title in v:
                ris_body += 'T2  - {st}\n'.format(st=title)

        elif k == 'volume':
            ris_body +=  'VL  - {vol}\n'.format(vol=v)

        elif k == 'issue':
            ris_body += 'IS  - {i}\n'.format(i=v)

        elif k == 'pages':
            pages = v.split("-")
            ris_body += 'SP  - {sp}\n'.format(sp=pages[0])
            ris_body += 'EP  - {ep}\n'.format(ep=pages[1])

        elif k == 'created':
            date_parts = v['date-parts']
            for date in date_parts:
                y = date[0]
                m = ''
                d = ''

                if len(date) > 1:
                    m = date[1]
                if len(date) > 2:
                    d = date[2]

                ris_body += 'Y1  - {y}/{d}/{m}\n'.format(y=y,d=d,m=m)

        elif k == 'link':
            for link in v:
                url = link['URL']
                ris_body += 'LK  - {url}\n'.format(url=url)

        elif k == 'subject':
            for subject in v:
                ris_body += 'RN  - {rn}\n'.format(rn=subject)

    ris_final = '{head}{body}{end}'.format(head=ris_header,
                                           body=ris_body,
                                           end=ris_end)

    return ris_final


def json2ris(in_json):

    """
    Converts a citation reference in JSON format into RIS.
    :param in_json: A bibligraphical reference in JSON format.
    :return: Python string containing the bibliographic information in RIS
    format.
    """

    pjson = json.loads(in_json)
    return dict2ris(pjson)
