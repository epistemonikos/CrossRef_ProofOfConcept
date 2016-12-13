__author__ = 'fmosso'

class JournalRating:
    def __init__(self, raw_cita, journal):
       self.cita = raw_cita or ''
       self.journal = journal or ''

    def value(self):
        return 1
