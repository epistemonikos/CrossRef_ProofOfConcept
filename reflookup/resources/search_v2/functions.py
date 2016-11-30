from threading import Thread

from flask_restful import abort

from reflookup.resources.lookup_functions.citation_search import \
    cr_citation_lookup, mendeley_lookup
from reflookup.utils.pubmed_id import getPubMedID
from reflookup.utils.rating.chooser import Chooser
from reflookup.utils.standardize_json import StandardDict


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
