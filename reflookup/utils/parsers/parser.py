from reflookup.utils.parsers.default_parser import DefaultParser
from reflookup.utils.parsers.bmc import BMCParser
from reflookup.utils.parsers.springer import SpringerParser
from reflookup.utils.parsers.wiley import WileyParser
from reflookup.utils.parsers.sciencedirect import ScienceDirectParser
from reflookup.utils.parsers.plos import PlosParser
import requests

class Parser:
    @staticmethod
    def parse(url):
        # En caso de que llegue un doi en vez de una url
        if url[:3] == "10.":
            url = "http://doi.org/" + url
        # Resolver el doi
        if "doi.org" in url:
            url = requests.get(url, allow_redirects=True).url

        # Ocupar el parser adecuado
        if "wiley" in url:
            parser = WileyParser()
        elif "springer" in url:
            parser = SpringerParser()
        elif "biomedcentral" in url:
            parser = BMCParser()
        elif "sciencedirect" in url:
            parser = ScienceDirectParser()
        elif "plos.org" in url:
            parser = PlosParser()
        else:
            parser = DefaultParser()
        return parser.parse(url)
