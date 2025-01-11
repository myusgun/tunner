# -*- coding: utf-8 -*-

#
# ressert -> re(stful a)ssert
#         -> re(sponse a)ssert
#

from misc import string
from tunner import useropt


def is_json_request(resp):
    return 'json' in resp.request.headers.get('Content-Type', '')


def is_json_response(resp):
    return 'json' in resp.headers.get('content-type', '')


def get_requested_api(resp):
    return f'{resp.request.method} {resp.request.path_url}'


def ressert(resp):
    if useropt.verbose(True) == 2:
        print(f'REQUEST -> {get_requested_api(resp)}')
        if is_json_request(resp):
            print(string.jsonify(resp.request.body))

    body = None

    try:
        body = resp.json()
    except:
        pass

    assert resp.ok, (resp, string.jsonify(body, False))
