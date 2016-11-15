from urllib.parse import unquote
from reflookup.utils.restful.utils import DeferredResource
from reflookup.utils.parsers.parser import Parser

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

    def post(self):
        data = self.post_parser.parse_args()
        url = unquote(data['url']).strip()
        return self.enqueue_job_and_return(Parser.parse, url)
