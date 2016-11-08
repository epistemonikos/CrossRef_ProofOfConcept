from urllib.parse import unquote

from reflookup.resources.lookup_functions.citation_extract import \
    pdf_extract_references
from reflookup.utils.restful.utils import DeferredResource
from werkzeug.datastructures import FileStorage

"""
This file contains the endpoint resources for retrieving references from a pdf file
"""

class ScopusReferenceExtractResource(DeferredResource):
    """
        This resource represents the /refs/pdf endpoint on the API.
    """

    def __init__(self):
        super().__init__()
        self.post_parser.add_argument('pdf_file', type=FileStorage, location='files')

    def post(self):
        data = self.post_parser.parse_args()
        return self.enqueue_task_and_return(pdf_extract_references, data)
