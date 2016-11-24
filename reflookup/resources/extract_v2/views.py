from flask_restful import abort
from werkzeug.exceptions import HTTPException

from reflookup.resources.lookup_functions.citation_extract import \
    get_scopus_references
from reflookup.utils.pubmed_id import getPubMedID
from reflookup.utils.restful.utils import DeferredResource
from reflookup.resources.lookup_functions.citation_extract import getRefID, \
    getReferenceInfo


class IntegratedReferenceExtractV2(DeferredResource):
    def __init__(self):
        super().__init__()
        self.get_parser.add_argument('doi', type=str, required=False,
                                     action='append')
        self.get_parser.add_argument('url', type=str, required=False,
                                     action='append')
        self.get_parser.add_argument('pmid', type=str, required=False,
                                     action='append')

    def get(self):
        args = self.get_parser.parse_args()

        dois = args['doi']
        urls = args['url']
        pmids = args['pmid']

        if not dois and not urls and not pmids:
            abort(400, message='Please provide at least one identifier '
                               '(DOI/PMID/URL) to extract references from.')

        return self.enqueue_job_and_return(extract_refs, dois, urls, pmids)


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
