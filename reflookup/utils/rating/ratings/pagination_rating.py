import re

class PaginationRating:

    def __init__(self, raw_cita, pagination):
        self.cita = raw_cita or ''
        self.pagination = pagination or ''

    def value(self):

        regex = r"[\b]" + re.escape(self.pagination) + r"[\b]"
        if re.search(regex, self.cita):
            return 1
        pages = self.pagination.split('-')
        if len(pages) == 2:
            if pages[0].isdigit() and pages[1].isdigit():
                len_diff = len(pages[1]) - len(pages[0])
                if len_diff < 0:
                    # 1234-45
                    pages[1] = pages[0][:len_diff*-1] + pages[1]
                    self.pagination = "{}-{}".format(pages[0], pages[1])
                    regex = r"[\b]" + re.escape(self.pagination) + r"[\b]"
                    if re.search(regex, self.cita):
                        return 1
        return 0
