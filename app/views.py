
import flask

from . import app


@app.route('/', methods=['GET'])
def test():
    f = {'a': 'b'}
    return flask.jsonify(**f)
