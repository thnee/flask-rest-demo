
import os
import pytest

from app import app as _app
from app import db as _db


TESTDB = 'test_project.db'
TESTDB_PATH = "/tmp/{}".format(TESTDB)
TEST_DATABASE_URI = 'sqlite:///' + TESTDB_PATH


@pytest.fixture(scope='session')
def app(request):
    """
    Create a Flask app, and override settings, for the whole test session.
    """

    _app.config.update(
        TESTING=True,
        SQLALCHEMY_DATABASE_URI=TEST_DATABASE_URI,
    )

    return _app


@pytest.fixture(scope='session')
def client(app, request):
    """
    Get the test_client from the app, for the whole test session.
    """
    return app.test_client()


@pytest.fixture()
def db(app, request):
    """
    Create entire database for every test.
    This could be optimized/extended, so that it creates the db once, and uses transactions for each test.
    """
    if os.path.exists(TESTDB_PATH):
        os.unlink(TESTDB_PATH)

    def teardown():
        _db.session.commit()
        _db.drop_all()
        os.unlink(TESTDB_PATH)

    _db.create_all()

    request.addfinalizer(teardown)
    return _db
