from rating.reference_helpers import cita_without_stop_words

class TitleRating:
    def __init__(self, raw_cita, raw_title):
        self.raw_cita = raw_cita
        self.raw_title = raw_title
    def value(self):
        if self.raw_title in self.raw_cita:
            return 1
        cita = cita_without_stop_words(self.raw_cita)
        title = cita_without_stop_words(self.raw_title).split(' ')
        matchs = [word for word in title if word in cita]
        rating = len(matchs)/len(title) if len(title) > 0 else 0
        # TODO: puntaje proporcional a la distancia entre las palabras con match
        return rating
