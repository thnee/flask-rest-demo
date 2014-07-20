
from flask_wtf import Form

from wtforms import StringField
from wtforms.validators import Email

from .form_mixins import ConditionalDataRequiredMixin
from .validators import ConditionalDataRequired


class UserForm(
    ConditionalDataRequiredMixin,
    Form
):
    email = StringField('email', validators=[ConditionalDataRequired(), Email()])
    password = StringField('password', validators=[ConditionalDataRequired()])
    name = StringField('name', validators=[ConditionalDataRequired()])
