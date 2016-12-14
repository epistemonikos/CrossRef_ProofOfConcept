class JournalRating:
    def __init__(self, raw_cita, journal):
        self.cita = raw_cita or ''
        self.pagination = journal or ''

    def value(self):
        print (self.pagination)
        print(self.cita)
        return 1