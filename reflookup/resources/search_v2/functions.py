import hashlib

from flask_restful import abort

from reflookup.resources.lookup_functions.citation_search import \
    cr_citation_lookup, mendeley_lookup
from reflookup.utils.pubmed_id import getPubMedID
from reflookup.utils.rating.chooser import Chooser
from reflookup.utils.standardize_json import StandardDict


def single_search(cit, cr_only=False, md_only=False, threshold=0.5):
    if cr_only and not md_only:
        return cr_citation_lookup(cit)

    elif md_only and not cr_only:
        return mendeley_lookup(cit)

    else:
        # results = {
        #     'mendeley': None,
        #     'crossref': None
        # }
        #
        # def cr_thread():
        #     results['crossref'] = cr_citation_lookup(cit)
        #
        # def md_thread():
        #     results['mendeley'] = mendeley_lookup(cit)
        #
        # t1 = Thread(target=cr_thread)
        # t2 = Thread(target=md_thread)
        #
        # t1.start()
        # t2.start()
        #
        # t1.join()
        # t2.join()
        #
        # cr = results.get('crossref', StandardDict().getEmpty())
        # md = results.get('mendeley', StandardDict().getEmpty())
        #
        # if not cr and not md:
        #     abort(404,
        #           message='No results found for query {}'.format(cit))
        # elif not md:
        #     return cr
        # elif not cr:
        #     return md
        # else:
        #     ch = Chooser(cit, [cr, md])
        #     return ch.select()

        cr_result = cr_citation_lookup(cit)
        not_cr = cr_result is None
        if not_cr:
            cr_result = StandardDict().getEmpty()

        result = cr_result
        if cr_result.get('rating', {}).get('total', 0.0) < threshold:
            md_result = mendeley_lookup(cit)
            not_md = md_result is None
            if not_cr and not_md:
                abort(404, message='No results found for query {}'.format(cit))

            if not_md:
                return cr_result
            ch = Chooser(cit, [cr_result, md_result])
            result = ch.select()

        result['md5'] = hashlib.md5(cit.encode('utf-8')).hexdigest()

        return result


def multi_search(citations, cr_only=False, md_only=False):
    results = []
    for citation in citations:
        results.append(single_search(citation, cr_only, md_only))

    return results


def deferred_search(citations, cr_only=False, md_only=False):
    results = multi_search(citations, cr_only, md_only)
    final = []
    for res in results:
        final.append(getPubMedID(res))

    return final
