from reflookup.utils.rating.ratings.authors_rating import AuthorsRating
from reflookup.utils.rating.ratings.title_rating import TitleRating

from reflookup.utils.rating.ratings.year_rating import YearRating


class Rating:
    def __init__(self, cita, json):
        self.cita = cita
        self.json = json

        authors_given = [aut.get('given', '') for aut in
                         json.get('authors', [])]
        authors_family = [aut.get('family', '') for aut in
                          json.get('authors', [])]
        year = json.get('publication_type', {}).get('title', '')
        title = json.get('title', '')
        self.authors_rating = AuthorsRating(cita, authors_given,
                                            authors_family)
        self.title_rating = TitleRating(cita, title)
        self.year_rating = YearRating(cita, year, title)

    def value(self, verbose=False):
        title_rating = self.title_rating.value()
        authors_rating = self.authors_rating.value()
        year_rating = self.year_rating.value()
        final_rating = title_rating * 0.55 + authors_rating * 0.1 + year_rating * 0.35
        if verbose:
            print(self.cita)
            print(self.json)
            print("authors: %s" % authors_rating)
            print("year: %s" % year_rating)
            print("t_rate: %s" % title_rating)
            print("final_rate: %s" % final_rating)
        return {
            'total': final_rating,
            'title': title_rating,
            'authors': authors_rating,
            'year': year_rating
        }
