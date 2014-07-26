
import factory
from factory.alchemy import SQLAlchemyModelFactory

from app import db
from app.models import User


class UserFactory(SQLAlchemyModelFactory):
    class Meta:
        model = User
        sqlalchemy_session = db.session

    id = factory.Sequence(lambda n: n)
    name = factory.Sequence(lambda n: u'User %d' % n)
    email = factory.Sequence(lambda n: u'%d@example.com' % n)
    password_hash = factory.sequence(lambda n: u'%d' % n)
