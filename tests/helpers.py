
from factories import UserFactory


def create_user(db, **kwargs):
    user = UserFactory.build(**kwargs)
    db.session.add(user)
    db.session.commit()
    return user
