
# http://flask.pocoo.org/snippets/54/

from werkzeug.security import generate_password_hash, check_password_hash

from . import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(500), unique=True)
    password_hash = db.Column(db.String(128))
    name = db.Column(db.String(500))

    def __repr__(self):
        return '<User %r>' % self.email

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
