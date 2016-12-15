from fuzzywuzzy import fuzz

class JournalRating:

    def __init__(self, raw_cita, journal):
        self.cita = raw_cita or ''
        self.journal = journal or ''

    def value(self):
        return  fuzz.token_set_ratio(self.journal,self.cita)/100