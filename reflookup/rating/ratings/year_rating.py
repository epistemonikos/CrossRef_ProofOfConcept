from reflookup.rating.reference_helpers import cita_without_stop_words

class YearRating:
    def __init__(self, raw_cita, year):
        self.cita = cita_without_stop_words(raw_cita)
        self.year = year
    def value(self):
        rates = [{
            'char' : '/',
            'val' : 1
        },{
            'char' : '-',
            'val' : 1
        },{
            'char' : ' ',
            'val' : 0.75
        },{
            'char' : '',
            'val' : 0.25
        }]
        for rate in rates:
            en_year = rate['char'] + self.year
            latin_year = self.year + rate['char']
            if en_year in self.cita:
                return rate['val'] if ((en_year+' ') in self.cita) or ((en_year+'.') in self.cita) else 0.5*rate['val']
            if latin_year in self.cita:
                return rate['val'] if (' '+latin_year) in self.cita else 0.5*rate['val']
        return 0
