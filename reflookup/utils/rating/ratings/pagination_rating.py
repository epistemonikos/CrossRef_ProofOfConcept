class PaginationRating:
    def __init__(self, raw_cita, pagination):
        self.cita = raw_cita or ''
        self.pagination = pagination or ''

    def value(self):
        #TODO: an aproximate string match for pagination and the cite
        return 1