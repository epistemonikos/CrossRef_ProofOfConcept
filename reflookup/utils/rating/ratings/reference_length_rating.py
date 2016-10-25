import math

class ReferenceLengthRating:

    def __init__(self, raw_cita):
        self.raw_cita = raw_cita

    def value(self):
        raw_cita_length = len(self.raw_cita or '')
        AVG_LENGTH = 220 #promedio de largo de una referencia normal
        if raw_cita_length >= AVG_LENGTH:
            raw_cita_length = AVG_LENGTH
        if raw_cita_length < 1:
            raw_cita_length = 1
        return  math.log10(raw_cita_length)/math.log10(AVG_LENGTH)
