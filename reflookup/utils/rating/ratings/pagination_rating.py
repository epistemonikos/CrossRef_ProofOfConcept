class JournalRating:
    def __init__(self, raw_cita, pagination):
        self.cita = raw_cita or ''
        self.pagination = pagination or ''

    def value(self):
        return 1