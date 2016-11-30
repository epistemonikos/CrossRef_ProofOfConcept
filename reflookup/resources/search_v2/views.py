from flask_restful import abort

from reflookup.utils.rating.chooser import Chooser
from reflookup.utils.restful.utils import DeferredResource, \
    b64_encode_response, find_pubmedid_wrapper
from reflookup.resources.lookup_functions.citation_search import \
    cr_citation_lookup, mendeley_lookup
from threading import Thread
from reflookup.utils.pubmed_id import getPubMedID

from reflookup.utils.standardize_json import StandardDict


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


def single_search(cit, cr_only=False, md_only=False, dont_choose=False):
    if cr_only and not md_only:
        return cr_citation_lookup(cit)

    elif md_only and not cr_only:
        return mendeley_lookup(cit)

    else:
        results = {
            'mendeley': None,
            'crossref': None
        }

        def cr_thread():
            results['crossref'] = cr_citation_lookup(cit)

        def md_thread():
            results['mendeley'] = mendeley_lookup(cit)

        t1 = Thread(target=cr_thread)
        t2 = Thread(target=md_thread)

        t1.start()
        t2.start()

        t1.join()
        t2.join()

        cr = results.get('crossref', StandardDict().getEmpty())
        md = results.get('mendeley', StandardDict().getEmpty())

        if not cr and not md:
            abort(404,
                  message='No results found for query {}'.format(cit))
        elif not md:
            return cr
        elif not cr:
            return md
        elif dont_choose:
            return [cr, md]
        else:
            ch = Chooser(cit, [cr, md])

            return ch.select()


def deferred_search(citations):
    results = []
    for citation in citations:
        results.append(getPubMedID(single_search(citation)))

    return results
