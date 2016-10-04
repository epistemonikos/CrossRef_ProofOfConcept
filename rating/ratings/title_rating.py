from rating.reference_helpers import without_stop_words

class TitleRating:
    def __init__(self, raw_cita, raw_title):
        self.raw_cita = raw_cita.lower()
        self.raw_title = raw_title.lower()
    def value(self):
        if self.raw_title in self.raw_cita:
            return 1
        cita = without_stop_words(self.raw_cita)
        title = without_stop_words(self.raw_title).split(' ')
        matchs = [word for word in title if word in cita]
        rating = len(matchs)/len(title) if len(title) > 0 else 0
        # TODO: puntaje proporcional a la distancia entre las palabras con match
        return rating
