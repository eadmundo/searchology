import os
from flask import render_template, redirect, url_for, abort, flash
from itsdangerous import URLSafeSerializer, BadSignature
from searchology.app.extensions.database import database as db
from searchology.db.models import BetaUsers
from searchology.app.extensions.login import current_user
from . import blueprint
from .forms import BetaEmailForm


@blueprint.route('/')
def beta_home():
    """"
    The beta home page
    """
    if current_user.is_authenticated():
        return redirect(url_for('users.dashboard'))
    return render_template('beta.jinja')

@blueprint.route('/activate/<code>', methods=('GET', 'POST'))
def activation(code):
    """
    The beta activation page
    """
    serializer = URLSafeSerializer(
        os.environ.get(
                'ITSDANGEROUS_SECRET_KEY', 'test-secret'))
    try:
        email = serializer.loads(code)
        # if for some reason the email de-serializes
        # but it's not in the database, then pretend it didn't work
        beta_user = db.session.query(
            BetaUsers).filter_by(email=email).first()
        if beta_user is None:
            return abort(404)
    # if the email doesn't de-serialize
    # then this is a bad signature
    except BadSignature:
        return abort(404)
    # otherwise it's a legitimate activation code
    form = BetaEmailForm(code=code)
    if form.validate_on_submit():
        # if they know which email it was sent to
        # then let them continue, otherwise let them try again
        if serializer.dumps(form.email.data.lower()) == form.code.data:
            return redirect(url_for('users.signup', code=code))
        else:
            flash('That doesn\'t seem to be the right email address - try again?', 'error')
    return render_template('confirm_email.jinja', form=form, code=code)
