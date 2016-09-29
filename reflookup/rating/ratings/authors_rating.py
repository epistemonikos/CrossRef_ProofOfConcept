class AuthorsRating:
    def __init__(self, raw_cita, authors_given, authors_family):
        self.raw_cita = raw_cita
        self.authors_given = authors_given
        self.authors_family = authors_family
    def value(self):
        authors = [{
            'full_name' : "%s %s" % (self.authors_family[i], self.authors_given[i]),
            'abrev_name' : "%s %s." % (self.authors_family[i], self.authors_given[i][0]),
            'abrev_name_2' : "%s, %s." % (self.authors_family[i], self.authors_given[i][0]),
            'given_name' : "%s" % (self.authors_given[i]),
            'familyname' : "%s" % (self.authors_family[i])
        } for i in range(len(self.authors_given))]
        raw_rating = 0
        for author in authors:
            raw_rating += self.author_rate(author, self.raw_cita)
        rating = raw_rating/len(authors) if len(authors) > 0 else 0
        return rating

    def author_rate(self, author, raw_cita):
        rates = [{
            'style' : 'full_name',
            'val' : 1
        },{
            'style' : 'abrev_name',
            'val' : 0.9
        },{
            'style' : 'abrev_name_2',
            'val' : 0.9
        },{
            'style' : 'given_name',
            'val' : 0.5
        },{
            'style' : 'familyname',
            'val' : 0.5
        }]
        cita = raw_cita.encode('ascii','ignore')
        for rate in rates:
            auth = author[rate['style']].encode('ascii','ignore')
            if auth in cita:
                # print("%s : %s" % (auth, rate['val']))
                return rate['val']
            # else:
            #     print("%s not in %s" % (auth, auth in cita))
        # print("%s : %s" % (author, 0))
        return 0
