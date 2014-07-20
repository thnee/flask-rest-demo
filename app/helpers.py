
from flask import jsonify


def json_response(data, code):
    resp = jsonify(data)
    resp.status_code = code
    return resp
