
from flask_wtf import Form

from wtforms import StringField
from wtforms.validators import DataRequired, Email


class UserForm(Form):
    email = StringField('email', validators=[DataRequired(), Email()])
    password = StringField('password', validators=[DataRequired()])
    name = StringField('name', validators=[DataRequired()])
