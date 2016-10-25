from reflookup.utils.rating.ratings.authors_rating import AuthorsRating
from reflookup.utils.rating.ratings.title_rating import TitleRating
from reflookup.utils.rating.ratings.year_rating import YearRating
from reflookup.utils.rating.ratings.reference_length_rating import ReferenceLengthRating

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
        self.reference_length_rating = ReferenceLengthRating(cita)

    def value(self):
        title_rating = self.title_rating.value()
        authors_rating = self.authors_rating.value()
        year_rating = self.year_rating.value()
        length_rating = self.reference_length_rating.value()
        final_rating = title_rating*0.65 + authors_rating*0.25 + year_rating*0.1
        final_rating *= length_rating
        return {
            'total': final_rating,
            'title': title_rating,
            'authors': authors_rating,
            'year': year_rating,
            'reference_length': length_rating
        }
