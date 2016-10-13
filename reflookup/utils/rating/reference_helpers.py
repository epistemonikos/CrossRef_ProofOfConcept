from stop_words import get_stop_words


def without_stop_words(raw):
    if not raw:
        return ''
    stop_words = get_stop_words('en')
    return ''.join([c for c in raw if c not in stop_words])
