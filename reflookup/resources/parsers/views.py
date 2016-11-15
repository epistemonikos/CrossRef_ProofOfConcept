from urllib.parse import unquote

from reflookup.resources.lookup_functions.citation_extract import \
    get_scopus_references
from reflookup.utils.restful.utils import DeferredResource
from reflookup.utils.pubmed_id import getPubMedID
from reflookup.resources.parsers.bmc import BMCParser
from reflookup.resources.parsers.springer import SpringerParser
from reflookup.resources.parsers.wiley import WileyParser

"""
This file contains the endpoint resources for retrieving information via parsers
"""

class ParserResource(DeferredResource):
    """
        This resource represents the /refs/scopus endpoint on the API.
    """

    def __init__(self):
        super().__init__()
        self.post_parser.add_argument('url', type=str, required=True,
                                      location='values')
        self.springer = SpringerParser()
        self.bmc = BMCParser()
        self.wiley = WileyParser()

    def post(self):
        data = self.post_parser.parse_args()
        url = unquote(data['url']).strip()

        if "wiley" in url:
            return self.enqueue_job_and_return(self.wiley.parse, url)
        elif "springer" in url:
            return self.enqueue_job_and_return(self.springer.parse, url)
        elif "biomedcentral" in url:
            return self.enqueue_job_and_return(self.bmc.parse, url)
        else:
            return "bla"
