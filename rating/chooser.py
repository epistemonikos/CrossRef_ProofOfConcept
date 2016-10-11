from rating.rating import Rating


class Chooser:
    def __init__(self, cita, jsons):
        self.jsons = jsons
        self.cita = cita

    def select(self):
        max_rating = 0
        best_json = {}
        for json in self.jsons:
            rating = Rating(self.cita, json)
            json['rating'] = rating.value()
            if rating > max_rating:
                max_rating = rating
                best_json = json
        # TODO: fusionar jsons si refieren a lo mismo que la mejor opción
        return best_json
