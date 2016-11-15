import traceback

from reflookup.utils.restful.utils import DeferredResource
from reflookup.resources.pubmed_extract.views import \
    deferred_extract_references as pmid_extract_refs
from reflookup.resources.scopus_extract.views import \
    deferred_extract_references as scopus_extract_refs
from flask_restful import HTTPException, abort

import threading


def threaded_ref_extract(extract_func, args, result_dict):
    try:
        r = extract_func(args)
        if len(r) < 1:
            abort(404, message='No references found for id {}'.format(args))
        else:
            result_dict['results'] = r
    except HTTPException as e:
        result_dict['results'] = None
        result_dict['code'] = e.code
        result_dict['description'] = e.data.get('message', '')


def deferred_extract_references(id_dict):
    result_dicts = []
    threads = []

    for key, value in id_dict.items():
        res = {'type': key}
        if not value:
            continue

        value = str(value)

        if key == 'doi':
            t = threading.Thread(target=threaded_ref_extract,
                                 args=(scopus_extract_refs, value, res))
        elif key == 'pubmed':
            t = threading.Thread(target=threaded_ref_extract,
                                 args=(pmid_extract_refs, value, res))
        else:
            continue

        t.start()
        threads.append(t)
        result_dicts.append(res)

    for t in threads:
        t.join()

    results = {}
    for d in result_dicts:
        if not d.get('results', False):
            results[d.get('type')] = {
                'error': '{code} - {desc}'.format(code=d.get('code'),
                                                  desc=d.get(
                                                      'description'))
            }
        else:
            results[d.get('type')] = d.get('results')

    return results


class IntegratedReferenceExtractResource(DeferredResource):
    def __init__(self):
        super().__init__()
        self.post_parser.add_argument('doi', type=str, required=False)
        self.post_parser.add_argument('pubmed', type=int, required=False)

    def post(self):
        data = self.post_parser.parse_args()
        return self.enqueue_job_and_return(deferred_extract_references, data)
