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
        ret_dict = {
            'length': 0,
            'result': []
        }

        if type(result) == list:
            for r in result:
                ret_dict['result'].append(getPubMedID(r))

            ret_dict['length'] = len(ret_dict['result'])

        else:
            ret_dict['result'].append(getPubMedID(result))
            ret_dict['length'] = 1

        return ret_dict

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
