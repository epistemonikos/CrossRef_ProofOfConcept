from werkzeug.exceptions import HTTPException

from reflookup.resources.lookup_functions.citation_extract import \
    get_scopus_references, getReferenceInfo, getRefID
from reflookup.utils.pubmed_id import getPubMedID


def extract_refs(dois, urls, pmids):
    results = {}

    def gen_error(id):
        return {'message': 'No references found for {}.'.format(id)}

    if dois:
        for doi in dois:
            results[doi] = []
            try:
                r = get_scopus_references(doi)
                refs = r.get('references', None)
                if not refs:
                    results[doi] = gen_error(doi)
                else:
                    for ref in refs:
                        results[doi].append(getPubMedID(ref))

            except HTTPException:
                results[doi] = gen_error(doi)
    if urls:
        for url in urls:
            results[url] = []
            try:
                r = get_scopus_references(url)
                refs = r.get('references', None)
                if not refs:
                    results[url] = gen_error(url)
                else:
                    for ref in refs:
                        results[url].append(getPubMedID(ref))

            except HTTPException:
                results[url] = gen_error(url)

    if pmids:
        for pmid in pmids:
            results[pmid] = []
            try:
                r = getReferenceInfo(getRefID(pmid))

                if not r:
                    results[pmid] = gen_error(pmid)
                else:
                    for ref in r:
                        results[pmid].append(ref)

            except HTTPException:
                results[pmid] = gen_error(pmid)

    return results
