from rating.reference_helpers import without_stop_words


class TitleRating:
    def __init__(self, raw_cita, raw_title):
        self.raw_cita = raw_cita or ''
        self.raw_title = raw_title or ''

    def value(self):
        cita = without_stop_words(self.raw_cita.lower())
        title = without_stop_words(self.raw_title.lower())
        if not (title and cita):
            return 0
        if (self.raw_title and self.raw_cita) and (self.raw_title in self.raw_cita):
            return 1
        title = title.split(' ')
        matchs = [word for word in title if word in cita]
        rating = len(matchs) / len(title) if len(title) > 0 else 0
        # TODO: puntaje proporcional a la distancia entre las palabras con match
        return rating
