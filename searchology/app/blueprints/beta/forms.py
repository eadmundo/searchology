from flask_wtf import Form
from wtforms import TextField, HiddenField
from wtforms.validators import Email


class BetaEmailForm(Form):
    email = TextField('email', validators=[Email()])
    code = HiddenField('code')
