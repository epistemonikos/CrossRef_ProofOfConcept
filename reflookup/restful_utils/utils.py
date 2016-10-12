from functools import wraps
from reflookup.pubmed_id import getPubMedID
from flask_restful import Resource


def find_pubmedid_wrapper(func):
    # wrapper function that adds pubmed id to requests
    @wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        return getPubMedID(result)

    return wrapper


class ExtResource(Resource):
    method_decorators = [find_pubmedid_wrapper]
