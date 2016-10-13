import re
from unidecode import unidecode


class AuthorsRating:
    def __init__(self, raw_cita, authors_given, authors_family):
        self.raw_cita = unidecode(raw_cita.lower())
        self.authors_given = []
        self.authors_family = []
        for x in authors_given:
            self.authors_given.append(unidecode(x.lower()) if x else '')

        for x in authors_family:
            self.authors_family.append(unidecode(x.lower()) if x else '')

    def full_name(self, family, given):
        return "%s %s" % (family, given) if given and family else None
    def abrev_name(self, family, given):
        return "%s, %s." % (family, given[0]) if given and family else None
    def abrev_name_2(self, family, given):
        return "%s %s." % (family, given[0]) if given and family else None

    def value(self):
        authors = [{
               'full_name': self.full_name(self.authors_family[i], self.authors_given[i]),
               'abrev_name': self.abrev_name(self.authors_family[i], self.authors_given[i]),
               'abrev_name_2': self.abrev_name_2(self.authors_family[i], self.authors_given[i]),
               'given_name': self.authors_given[i],
               'familyname': self.authors_family[i]
           } for i in range(len(self.authors_given))]
        raw_rating = 0
        matchs = 0
        for author in authors:
            author_rating = self.author_rate(author, self.raw_cita)
            if author_rating != 0:
                matchs += 1
                raw_rating += author_rating
        if re.search(r"\set\sal[^\w]", self.raw_cita):
            return raw_rating / matchs if matchs > 0 else 0
        else:
            return raw_rating / len(authors) if len(authors) > 0 else 0

    @staticmethod
    def author_rate(author, raw_cita):
        rates = [{
            'style': 'full_name',
            'val': 1
        }, {
            'style': 'abrev_name',
            'val': 1
        }, {
            'style': 'abrev_name_2',
            'val': 1
        }, {
            'style': 'given_name',
            'val': 0.5
        }, {
            'style': 'familyname',
            'val': 0.9
        }]
        cita = raw_cita.encode('ascii', 'ignore')
        for rate in rates:
            auth = (author[rate['style']] or '').encode('ascii', 'ignore')
            if auth and auth in cita:
                return rate['val']
        return 0
