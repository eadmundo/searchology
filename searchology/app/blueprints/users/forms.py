from flask.ext.wtf import (
    Form, TextField, HiddenField,
    PasswordField, Optional, validators
)
from searchology.db.models import Users

# Maximum length of the username & email address as specified by the database object. Used to
# restrict the max length of the fields in the forms.
MAX_LENGTH_USERNAME = Users.username.property.columns[0].type.length
# MAX_LENGTH_EMAIL = Users.email.property.columns[0].type.length


class SignUpForm(Form):
    email = TextField('Email address', validators=[validators.Email()])
    username = TextField('Username', validators=[validators.InputRequired()])
    passphrase = PasswordField('Passphrase', validators=[validators.InputRequired()])


class LoginForm(Form):
    username = TextField('Username', validators=[validators.InputRequired()])
    passphrase = PasswordField('Passphrase', validators=[validators.InputRequired()])
    next = HiddenField(validators=[Optional()])
