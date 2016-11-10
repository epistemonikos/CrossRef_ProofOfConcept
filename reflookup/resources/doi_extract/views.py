import requests

from reflookup.utils.restful.utils import DeferredResource
from reflookup.resources.doi_extract.scihub import SciHub
from uuid import uuid4
from reflookup.resources.lookup_functions.citation_extract import \
    pdf_extract_references


def download_and_parse(doi):
    sh = SciHub()
    filepath = '/tmp/' + str(uuid4())
    sh.download(doi, path=filepath)

    return pdf_extract_references(filepath)


class DoiExtractReferences(DeferredResource):
    def __init__(self):
        super().__init__()
        self.post_parser.add_argument('doi', required=True, location='values',
                                      type=str)

    def post(self):
        doi = self.post_parser.parse_args()['doi']
        return self.enqueue_job_and_return(download_and_parse, doi)
