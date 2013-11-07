from flask.ext.wtf import Form, TextField, HiddenField, PasswordField, Required, Optional, validators, ValidationError
from searchology.db.models import Users

# Maximum length of the username & email address as specified by the database object. Used to
# restrict the max length of the fields in the forms.
MAX_LENGTH_USERNAME = Users.username.property.columns[0].type.length
# MAX_LENGTH_EMAIL = Users.email.property.columns[0].type.length


class LoginForm(Form):
    username = TextField('Username', validators=[Required(), validators.length(max=MAX_LENGTH_USERNAME)])
    passphrase = PasswordField('Passphrase', validators=[Required()])
    next = HiddenField(validators=[Optional()])
