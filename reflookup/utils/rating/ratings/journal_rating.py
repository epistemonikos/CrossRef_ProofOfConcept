class JournalRating:
    def __init__(self, raw_cita, journal):
        self.cita = raw_cita or ''
        self.pagination = journal or ''

    def value(self):
        #TODO: an aproximate string match for journal and the cite
        return 1