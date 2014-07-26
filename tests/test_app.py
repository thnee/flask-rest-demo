
import json

from app.models import User
from helpers import create_user


headers = {'Content-Type': 'application/json'}


def test_get_all_users(client, db):
    # create 3 users
    users = [create_user(db) for _ in xrange(3)]

    # get all users
    r = client.get('/user')
    assert r.status_code == 200

    # ensure that it returns the same data (assume that the order of the objects are the same)
    data = json.loads(r.data)
    assert len(data['objects']) == 3
    for i in xrange(3):
        assert data['objects'][i]['id'] == users[i].id
        assert data['objects'][i]['email'] == users[i].email
        assert data['objects'][i]['name'] == users[i].name


def test_get_user(client, db):
    # create one user
    user = create_user(db)

    # get user based on id
    r = client.get('/user/{}'.format(user.id))
    assert r.status_code == 200

    # ensure that it returns the same data
    data = json.loads(r.data)
    assert data['id'] == user.id
    assert data['email'] == user.email
    assert data['name'] == user.name


def test_create_user_bad_requests(client, db):
    # no valid json header present
    r = client.post('/user')
    assert r.status_code == 400

    # json header, but not json data
    r = client.post('/user', headers=headers, data='not_json')
    assert r.status_code == 400


def test_create_user(client, db):
    # ensure that creating a user works
    r = client.post('/user', headers=headers, data=json.dumps({
        'name': 'asdf',
        'email': 'asdf@asdf.asdf',
        'password': 'asdf'
    }))
    assert r.status_code == 201

    # ensure that it returns the same data
    data = json.loads(r.data)
    assert int(data['id'])
    assert data['email'] == 'asdf@asdf.asdf'
    assert data['name'] == 'asdf'

    # ensure data has been updated in database
    user = User.query.first()
    assert user.id == data['id']
    assert user.email == 'asdf@asdf.asdf'
    assert user.name == 'asdf'
    assert user.check_password('asdf')


def test_update_user_full(client, db):
    # create one user
    user = create_user(db)
    user_id = user.id

    # update user with new data
    r = client.put('/user/{}'.format(user.id), headers=headers, data=json.dumps({
        'name': 'qwer',
        'email': 'qwer@qwer.qwer',
        'password': 'qwer',
    }))
    assert r.status_code == 204

    # get user again
    user = User.query.first()

    # ensure data has been updated in database
    assert user.id == user_id
    assert user.email == 'qwer@qwer.qwer'
    assert user.name == 'qwer'
    assert user.check_password('qwer')


def test_update_user_partial(client, db):
    # create one user
    user = create_user(db, email='abcd')
    user_id = user.id
    user.set_password('abcd')

    # ensure that partially updating user works
    r = client.patch('/user/{}'.format(user.id), headers=headers, data=json.dumps({
        'name': 'zxcv',
    }))
    assert r.status_code == 204

    # get user again
    user = User.query.first()

    # ensure name is updated
    assert user.name == 'zxcv'

    # ensure other fields are the same as before update
    assert user.id == user_id
    assert user.email == 'abcd'
    assert user.check_password('abcd')


def test_delete_user(client, db):
    # create one user
    user = create_user(db)

    # delete user based on id
    r = client.delete('/user/{}'.format(user.id))
    assert r.status_code == 204

    # ensure user is deleted
    users = db.session.query(User).all()
    assert len(users) == 0
