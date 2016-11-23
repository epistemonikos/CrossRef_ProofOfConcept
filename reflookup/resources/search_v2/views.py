from reflookup.utils.restful.utils import DeferredResource, \
    b64_encode_response, find_pubmedid_wrapper
from reflookup.resources.lookup_functions.citation_search import \
    cr_citation_lookup, mendeley_lookup
from threading import Thread


class IntegratedReferenceSearchV2(DeferredResource):
    method_decorators = []

    def __init__(self):
        super().__init__()
        self.get_parser.add_argument('q', required=True, type=str)
        self.get_parser.add_argument('cr_only', required=False, type=bool,
                                     default=False)
        self.get_parser.add_argument('md_only', required=False, type=bool,
                                     default=False)
        self.get_parser.add_argument('dont_choose', required=False, type=bool,
                                     default=False)

    @find_pubmedid_wrapper
    def get(self):
        args = self.get_parser.parse_args()
        citation = args['q']

        if args['cr_only'] and not args['md_only']:
            return cr_citation_lookup(citation)

        elif args['md_only'] and not args['cr_only']:
            return mendeley_lookup(citation)

        else:
            results = {
                'mendeley': None,
                'crossref': None
            }

            def cr_thread():
                try:
                    results['crossref'] = cr_citation_lookup(citation)
                finally:
                    pass

            def md_thread():
                try:
                    results['mendeley'] = mendeley_lookup(citation)
                finally:
                    pass

            t1 = Thread(target=cr_thread())
            t2 = Thread(target=md_thread())

            t1.start()
            t2.start()

            t1.join()
            t2.join()
