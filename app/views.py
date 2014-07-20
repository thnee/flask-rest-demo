
from flask import request, Response, jsonify
from sqlalchemy import exists
from werkzeug.datastructures import MultiDict

from . import app, db

from .models import User
from .forms import UserForm
from .serializers import serialize_user, deserialize_user
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

    # check if user exists
    if user is None:
        return json_response({'error': 'No user exists with this id.'}, 404)

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

    return json_response(serialize_user(user), 201)


@app.route('/user/<int:user_id>', methods=['PUT', 'PATCH'])
def user_update(user_id):
    """
    Updates an existing user in the database.
    But first validate input data with UserForm, and check if email exists.
    """
    data = request.get_json()

    user = User.query.get(user_id)

    # check if user exists
    if user is None:
        return json_response({'error': 'No user exists with this id.'}, 404)

    # if PUT, all fields are required - if PATCH, none of the fields are required
    data_required = (request.method != 'PATCH')

    # validate input data
    form = UserForm(MultiDict(data), data_required=data_required)
    if not form.validate():
        return json_response(form.errors, 400)

    # check if email already exists
    if 'email' in data:
        email_exists = db.session.query(exists().where(User.email == data['email'])).scalar()
        if email_exists:
            return json_response({'email': 'This email address already exists.'}, 400)

    # deserialize data and save user object
    user, changed = deserialize_user(user, data)
    if changed:
        db.session.commit()

    return Response('', 204)


@app.route('/user/<int:user_id>', methods=['DELETE'])
def user_delete(user_id):

    user = User.query.get(user_id)

    # check if user exists
    if user is None:
        return json_response({'error': 'No user exists with this id.'}, 404)

    # delete user object
    user = User.query.get(user_id)
    db.session.delete(user)
    db.session.commit()

    return Response('', status=204)
