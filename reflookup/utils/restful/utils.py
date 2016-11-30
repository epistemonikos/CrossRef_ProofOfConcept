import base64
from datetime import datetime, timezone
from functools import wraps

import redis
from flask import json
from flask import make_response
from flask import request
from flask_restful import Resource, abort
from flask_restful.reqparse import RequestParser
from itsdangerous import BadSignature

from reflookup import app, rq, taskserializer
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


class DeferredResource(EncodingResource):
    """
    Base Resource for deferred results resources.
    """

    def __init__(self):
        self.post_parser = RequestParser()
        self.get_parser = RequestParser()

        self.result_ttl = app.config['RESULT_TTL_SECONDS']

    def enqueue_job_and_return(self, function, *args):
        try:
            job = rq.enqueue(function, *args, result_ttl=self.result_ttl)
            return {
                       'job': taskserializer.dumps(job.id),
                       'submitted': datetime.now(timezone.utc).isoformat()
                   }, 202

        except redis.exceptions.ConnectionError:
            abort(500)

    def check_job(self, job_id):
        try:
            job_id = taskserializer.loads(job_id)
        except BadSignature:
            abort(400, message='Invalid job id')

        job = rq.fetch_job(job_id)
        if not job:
            abort(404, message='No such job, or job discarded on TTL timeout.')

        if job.exc_info:
            # error
            return {
                       'done': True,
                       'result': {
                           'message': (job.exc_info.data.get('message', 'Unknown Error') if hasattr(job.exc_info, 'data') else 'Unknown Error')
                       },
                       'length': -1,
                       'result_ttl': 0,
                       'timestamp': datetime.now().isoformat(),
                   }, 400

        elif not job.result:
            return {
                       'done': False,
                       'result': None,
                       'length': 0,
                       'result_ttl': self.result_ttl,
                       'timestamp': None
                   }, 202
        else:
            result = job.result if type(job.result) == list else [job.result]
            return {
                       'done': True,
                       'result': result,
                       'length': len(result),
                       'result_ttl': self.result_ttl,
                       'timestamp': job.ended_at.isoformat()
                   }, 200
