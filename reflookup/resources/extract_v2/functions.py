from werkzeug.exceptions import HTTPException

from reflookup.resources.lookup_functions.citation_extract import \
    get_scopus_references, getReferenceInfo, getRefID
from reflookup.utils.pubmed_id import getPubMedID


def extract_refs(dois, urls, pmids):
    results = []

    def gen_error(id):
        return {'message': 'No references found for {}.'.format(id)}

    if dois:
        for doi in dois:
            try:
                r = get_scopus_references(doi)
                results.append(getPubMedID(r))
            except HTTPException:
                results.append(gen_error(doi))
    if urls:
        for url in urls:
            try:
                r = get_scopus_references(url)
                results.append(getPubMedID(r))
            except HTTPException:
                results.append(gen_error(url))

    if pmids:
        for pmid in pmids:
            try:
                r = getReferenceInfo(getRefID(pmid))
                results.append(r)
            except HTTPException:
                results.append(gen_error(pmid))

    return results
