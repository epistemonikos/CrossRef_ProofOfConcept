import base64
from functools import wraps

from flask import json
from flask import make_response
from flask import request
from flask_restful import Resource

from reflookup.utils.pubmed_id import getPubMedID


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

    return b64_encode_response(wrapper)


def b64_encode_response(func):
    # wrapper to automatically base64 encode response
    @wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        headers = request.headers

        if headers.get('Accept-Encoding', False) == 'base64':
            code = 200
            if type(result) == tuple:
                result, code = result

            result64 = base64.b64encode(json.dumps(result).encode())
            headers = {
                'Content-Type': 'application/json',
                'Content-Encoding': 'base64'
            }

            return make_response(result64, code, headers)
        else:
            return result

    return wrapper


class EncodingResource(Resource):
    method_decorators = [b64_encode_response]


class ExtResource(EncodingResource):
    method_decorators = [find_pubmedid_wrapper]
