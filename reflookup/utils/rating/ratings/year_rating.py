
import re


class YearRating:
    def __init__(self, raw_cita, year, raw_title):
        self.cita = raw_cita or ''
        self.title = raw_title or ''
        self.year = str(year or '')

    def value(self):
        if not self.year:
            return 0
        year = r'[\.\s\(^]'+re.escape(self.year)+'[\.\s\)]'
        if re.search(year, self.cita):
            if re.search(year, self.title):
                # TODO: ver si está igual en la cita, porque podria estar 2 veces.
                return 0.8
            return 1
        return 0