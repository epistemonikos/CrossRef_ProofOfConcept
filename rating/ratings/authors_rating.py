import re
from unidecode import unidecode
class AuthorsRating:
    def __init__(self, raw_cita, authors_given, authors_family):
        self.raw_cita = unidecode(raw_cita.lower())
        self.authors_given = [unidecode(x.lower()) for x in authors_given]
        self.authors_family = [unidecode(x.lower()) for x in authors_family]
    def value(self):
        authors = [{
            'full_name' : "%s %s" % (self.authors_family[i], self.authors_given[i]),
            'abrev_name' : "%s %s." % (self.authors_family[i], self.authors_given[i][0]),
            'abrev_name_2' : "%s, %s." % (self.authors_family[i], self.authors_given[i][0]),
            'given_name' : "%s" % (self.authors_given[i]),
            'familyname' : "%s" % (self.authors_family[i])
        } for i in range(len(self.authors_given)) if self.authors_family[i] or self.authors_given[i]]
        raw_rating = 0
        matchs = 0
        for author in authors:
            author_rating = self.author_rate(author, self.raw_cita)
            if author_rating != 0:
                matchs += 1
                raw_rating += author_rating
        if re.search(r"\set\sal[^\w]", self.raw_cita):
            return raw_rating/matchs if matchs > 0 else 0
        else:
            return raw_rating/len(authors) if len(authors) > 0 else 0
    def author_rate(self, author, raw_cita):
        rates = [{
            'style' : 'full_name',
            'val' : 1
        },{
            'style' : 'abrev_name',
            'val' : 1
        },{
            'style' : 'abrev_name_2',
            'val' : 1
        },{
            'style' : 'given_name',
            'val' : 0.5
        },{
            'style' : 'familyname',
            'val' : 0.9
        }]
        cita = raw_cita.encode('ascii','ignore')
        for rate in rates:
            auth = author[rate['style']].encode('ascii','ignore')
            if auth in cita:
                return rate['val']
        return 0
