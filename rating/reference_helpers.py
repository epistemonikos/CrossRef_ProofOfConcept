from stop_words import get_stop_words

def cita_without_stop_words(raw_cita):
    stop_words = get_stop_words('en')
    return ''.join([c for c in raw_cita if c not in stop_words])
