from rating.rating import Rating
from reflookup.standardize_json import StandardDict


class Chooser:
    def __init__(self, cita, jsons):
        self.jsons = jsons
        self.cita = cita

    def select(self):
        max_rating = 0
        best_json = StandardDict().getEmpty()
        for json in self.jsons:
            rating = Rating(self.cita, json)
            json['rating'] = rating.value()
            if rating.value()['total'] > max_rating:
                max_rating = rating.value()['total']
                best_json = json
        # TODO: fusionar jsons si refieren a lo mismo que la mejor opción
        return best_json
