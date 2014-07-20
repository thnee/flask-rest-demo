
from flask import request, Response, jsonify
from sqlalchemy import exists
from werkzeug.datastructures import MultiDict

from . import app, db

from .models import User
from .forms import UserForm
from .serializers import serialize_user
from .helpers import json_response


@app.route('/user', methods=['GET'])
def user_read():
    """
    Read all users from database.
    """
    users = User.query.all()
    return jsonify(objects=[serialize_user(user) for user in users])


@app.route('/user/<int:user_id>', methods=['GET'])
def user_read_single(user_id):
    """
    Read one user from database, based on user_id.
    """
    user = User.query.get(user_id)
    return jsonify(**serialize_user(user))


@app.route('/user', methods=['POST'])
def user_create():
    """
    Create new user in database.
    But first validate input data with UserForm, and check if email exists.
    """
    data = request.get_json()

    # validate input data
    form = UserForm(MultiDict(data))
    if not form.validate():
        return json_response(form.errors, 400)

    # check if email already exists
    email_exists = db.session.query(exists().where(User.email == data['email'])).scalar()
    if email_exists:
        return json_response({'email': 'This email address already exists.'}, 400)

    # create new user object
    user = User(data['email'], data['password'], data['name'])
    db.session.add(user)
    db.session.commit()

    return Response('', 200)

