from reflookup.utils.rating.ratings.authors_rating import AuthorsRating
from reflookup.utils.rating.ratings.title_rating import TitleRating
from reflookup.utils.rating.ratings.year_rating import YearRating
from reflookup.utils.rating.ratings.journal_rating import JournalRating
from reflookup.utils.rating.ratings.pagination_rating import PaginationRating


class Rating:
    def __init__(self, cita, json):
        self.cita = cita
        self.json = json

        authors_given = [aut.get('given', '') for aut in
                         json.get('authors', [])]
        authors_family = [aut.get('family', '') for aut in
                          json.get('authors', [])]
        year = json.get('publication_type', {}).get('year', '')
        journal = json.get('publication_type', {}).get('title', '')
        pagination = json.get('publication_type', {}).get('pagination', '')
        title = json.get('title', '')
        self.authors_rating = AuthorsRating(cita, authors_given,
                                            authors_family)
        self.title_rating = TitleRating(cita, title)
        self.year_rating = YearRating(cita, year, title)
        #self.journal_rating = JournalRating(cita,journal)
        self.journal_rating = TitleRating(cita, journal)
        self.pagination_rating = PaginationRating(cita,pagination)

    def value(self, verbose=False):
        title_rating = self.title_rating.value()
        authors_rating = self.authors_rating.value()
        year_rating = self.year_rating.value()
        journal_rating = self.journal_rating.value()
        pagination_rating = self.pagination_rating.value()

        #Rating ponderations
        if journal_rating <= 0.2 or pagination_rating <= 0.2:
            final_rating = title_rating * 0.55 + authors_rating * 0.1 + year_rating * 0.35
        else:
            final_rating = title_rating * 0.35 + authors_rating * 0.1 + year_rating * 0.2 +journal_rating* 0.2 + pagination_rating * 0.15

        if verbose:
            print(self.cita)
            print(self.json)
            print("pagination: %s" % pagination_rating)
            print("journal: %s" % journal_rating)
            print("authors: %s" % authors_rating)
            print("year: %s" % year_rating)
            print("t_rate: %s" % title_rating)
            print("final_rate: %s" % final_rating)
        return {
            'total': final_rating,
            'title': title_rating,
            'authors': authors_rating,
            'year': year_rating,
            'pagination': pagination_rating
            #'journal': journal_rating
        }
