
def serialize_user(user):
    return {
        'id': user.id,
        'email': user.email,
        'name': user.name,
    }
