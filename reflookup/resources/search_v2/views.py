from reflookup.resources.search_v2.functions import single_search, \
    deferred_search
from reflookup.utils.restful.utils import DeferredResource, \
    b64_encode_response, find_pubmedid_wrapper


class IntegratedReferenceSearchV2(DeferredResource):
    method_decorators = []

    def __init__(self):
        super().__init__()
        self.get_parser.add_argument('q', required=True, type=str,
                                     action='append')
        self.get_parser.add_argument('cr_only', required=False, type=bool,
                                     default=False)
        self.get_parser.add_argument('md_only', required=False, type=bool,
                                     default=False)
        self.get_parser.add_argument('dont_choose', required=False, type=bool,
                                     default=False)

    def get(self):
        args = self.get_parser.parse_args()
        cit = args['q']

        if len(cit) == 1:
            return find_pubmedid_wrapper(single_search)(cit[0],
                                                        args['cr_only'],
                                                        args['md_only'],
                                                        args['dont_choose'])
        else:
            return b64_encode_response(self.enqueue_job_and_return)(
                deferred_search, cit)


