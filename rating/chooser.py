from rating.rating import Rating

class Chooser:
    def __init__(self, cita, jsons):
        self.jsons = jsons
    def select():
        max_rating = 0
        best_json = {}
        for json in self.jsons:
            rating = Rating(cita, json)
            json['rating'] = rating.value()
            if rating > max_rating:
                max_rating = rating
                best_json = json
        # TODO: fucionar jsons si refieren a lo mismo que la mejor opción
        return best_json
