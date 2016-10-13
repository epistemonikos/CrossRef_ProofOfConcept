from functools import wraps
from reflookup.pubmed_id import getPubMedID
from flask_restful import Resource


def find_pubmedid_wrapper(func):
    # wrapper function that adds pubmed id to requests
    @wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        if not result.get('list_result', False):
            return getPubMedID(result)
        else:
            nresults = []
            for r in result.get('results', []):
                nresults.append(getPubMedID(r))
            result['results'] = nresults
            return result

    return wrapper


class ExtResource(Resource):
    method_decorators = [find_pubmedid_wrapper]
