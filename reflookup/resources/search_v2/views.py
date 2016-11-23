from flask.ext.restful import abort

from reflookup.utils.rating.chooser import Chooser
from reflookup.utils.restful.utils import DeferredResource, \
    b64_encode_response, find_pubmedid_wrapper
from reflookup.resources.lookup_functions.citation_search import \
    cr_citation_lookup, mendeley_lookup
from threading import Thread

from reflookup.utils.standardize_json import StandardDict


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
                results['crossref'] = cr_citation_lookup(citation)

            def md_thread():
                results['mendeley'] = mendeley_lookup(citation)

            t1 = Thread(target=cr_thread())
            t2 = Thread(target=md_thread())

            t1.start()
            t2.start()

            t1.join()
            t2.join()

            cr = results.get('crossref', None)
            md = results.get('mendeley', None)

            if not cr and not md:
                abort(404,
                      message='No results found for query {}'.format(citation))
            elif not md:
                return cr
            elif not cr:
                return md
            elif args['dont_choose']:
                return [cr, md]
            else:
                ch = Chooser(citation,
                             [cr.get('result', StandardDict().getEmpty()),
                              md.get('result', StandardDict().getEmpty())])

                return ch.select()
