from reflookup.utils.parsers.default_parser import DefaultParser
from reflookup.utils.parsers.bmc import BMCParser
from reflookup.utils.parsers.springer import SpringerParser
from reflookup.utils.parsers.wiley import WileyParser

def parse(url):
    if "wiley" in url:
        parser = WileyParser()
    elif "springer" in url:
        parser = SpringerParser()
    elif "biomedcentral" in url:
        parser = BMCParser()
    else:
        parser = DefaultParser()
    return parser.parse(url)
