
def serialize_user(user):
    return {
        'id': user.id,
        'email': user.email,
        'name': user.name,
    }


def deserialize_user(user, data):
    changed = False

    if 'email' in data:
        user.email = data['email']
        changed = True

    if 'password' in data:
        user.set_password(data['password'])
        changed = True

    if 'name' in data:
        user.name = data['name']
        changed = True

    return user, changed
