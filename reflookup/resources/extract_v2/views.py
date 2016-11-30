from flask_restful import abort

from reflookup.resources.extract_v2.functions import extract_refs
from reflookup.utils.restful.utils import DeferredResource


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


