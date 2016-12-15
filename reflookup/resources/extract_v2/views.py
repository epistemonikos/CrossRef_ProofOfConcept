from flask_restful import abort

from reflookup.auth.models import auth_required
from reflookup.resources.extract_v2.functions import extract_refs
from reflookup.utils.restful.utils import DeferredResource


class IntegratedReferenceExtractV2(DeferredResource):
    """
    Endpoint for extracting references from a given list of identifiers.
    Returns a job containing the result of the query in the format
    {
        '<id_1>': [ <list of references> ],
        '<id_2>': [ <list of references> ],
        ...
    }

    The endpoint aggregates all the given id's in lists, so the request can
    contain multiple queries for the same type of id. For example:

    <url>?doi=32424.32344?doi=34234?doi=sdf.23123

    Is treated as

    dois = ['32424.32344', '34234', 'sdf.23123']
    """

    def __init__(self):
        super().__init__()
        self.get_parser.add_argument('doi', type=str, required=False,
                                     action='append')
        self.get_parser.add_argument('url', type=str, required=False,
                                     action='append')
        self.get_parser.add_argument('pmid', type=str, required=False,
                                     action='append')

    @auth_required()
    def get(self):
        args = self.get_parser.parse_args()

        dois = args['doi']
        urls = args['url']
        pmids = args['pmid']

        if not dois and not urls and not pmids:
            abort(400, message='Please provide at least one identifier '
                               '(DOI/PMID/URL) to extract references from.')

        return self.enqueue_job_and_return(extract_refs, dois, urls, pmids)


