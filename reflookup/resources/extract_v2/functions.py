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
                for ref in r.get('references', []):
                    results[doi].append(getPubMedID(ref))

            except HTTPException:
                results[doi] = gen_error(doi)
    if urls:
        for url in urls:
            results[url] = []
            try:
                r = get_scopus_references(url)
                for ref in r.get('references', []):
                    results[url].append(getPubMedID(ref))

            except HTTPException:
                results[url] = gen_error(url)

    if pmids:
        for pmid in pmids:
            results[pmid] = []
            try:
                r = getReferenceInfo(getRefID(pmid))
                for ref in r:
                    results[pmid].append(ref)
            except HTTPException:
                results[pmid] = gen_error(pmid)

    return results
