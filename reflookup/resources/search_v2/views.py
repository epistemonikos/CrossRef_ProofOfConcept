from reflookup.resources.search_v2.functions import single_search, \
    multi_search, deferred_search
from reflookup.utils.restful.utils import DeferredResource, \
    b64_encode_response, find_pubmedid_wrapper


class IntegratedReferenceSearchV2(DeferredResource):
    """
    Endpoint for converting a plain text reference string into a JSON structure
    through searching in multiple reference services for the best match.

    This endpoint can work both in instant and deferred fashion:

    - If the request contains only one query, it is handled instantly.
    - Else, the request returns a job containing the results for the query, a
    list of JSONs.

    If the request is for only one reference, it can also include some optional
    parameters:

    - cr_only=true indicates to only return the top result from CrossRef.
    - md_only=true indicates to only return the top result from Mendeley.
    - dont_choose=true indicates to not choose the best result from the results
    of Crossref and Mendeley, and to return both.
    """

    method_decorators = []

    def __init__(self):
        super().__init__()
        self.get_parser.add_argument('q', required=True, type=str,
                                     action='append')
        self.get_parser.add_argument('cr_only', required=False, type=bool,
                                     default=False)
        self.get_parser.add_argument('md_only', required=False, type=bool,
                                     default=False)
        self.get_parser.add_argument('sync', required=False, type=bool,
                                     default=False)

        self.post_parser.add_argument('q', required=True, type=list,
                                      location='json')
        self.post_parser.add_argument('cr_only', required=False, type=bool,
                                      default=False, location='json')
        self.post_parser.add_argument('md_only', required=False, type=bool,
                                      default=False, location='json')
        self.post_parser.add_argument('sync', required=False, type=bool,
                                      default=False, location='json')

    def search(self, args):
        cit = args['q']
        if args['sync']:
            return find_pubmedid_wrapper(multi_search)(cit,
                                                       args['cr_only'],
                                                       args['md_only'])
        else:
            return b64_encode_response(self.enqueue_job_and_return)(
                deferred_search, cit, args['cr_only'], args['md_only'])

    def get(self):
        args = self.get_parser.parse_args()
        return self.search(args)

    def post(self):
        args = self.post_parser.parse_args()
        return self.search(args)
