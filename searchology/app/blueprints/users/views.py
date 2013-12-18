import os
from flask import redirect, request, url_for, flash, render_template, abort
from flask.ext.login import current_user, login_user, logout_user, login_required
from itsdangerous import URLSafeSerializer, BadSignature
from searchology.app.blueprints.users.forms import LoginForm
from searchology.app.blueprints.users import blueprint
from searchology.app.extensions.database import database
from searchology.db.models import Users
from searchology.db import session_scope
from .forms import SignUpForm


@blueprint.route('/login/', methods=['GET', 'POST'])
def login():
    """
    Logs the user in.
    """

    #next = request.args.get('next')
    form = LoginForm()

    # Handle case where user is already logged in
    if current_user.is_authenticated():
        return redirect(request.args.get('next') or url_for('beta.beta_home'))

    # Log user in
    if form.validate_on_submit():
        user = database.session.query(Users).filter_by(username=request.form['username']).first()
        if user is not None and user.passphrase_matches(request.form['passphrase']):
            login_user(user)
            return redirect(request.args.get('next') or url_for('.dashboard'))
        else:
            flash('Login failed', 'error')

    return render_template('login.jinja', form=form)


@blueprint.route('/signup/', methods=['GET', 'POST'])
@blueprint.route('/signup/<code>', methods=['GET', 'POST'])
def signup(code=None):

    serializer = URLSafeSerializer(
        os.environ.get(
                'ITSDANGEROUS_SECRET_KEY', 'test-secret'))

    email_from_code = None

    if code is not None:
        try:
            email_from_code = serializer.loads(code)
            email = email_from_code
        except BadSignature:
            return abort(404)
    else:
        email = ''

    form = SignUpForm(email=email)

    if form.validate_on_submit():
        email_confirmed = False
        if email_from_code is not None and form.email.data == email_from_code:
            email_confirmed = True
        user = Users(
            username=form.username.data,
            email=form.email.data,
            email_confirmed=email_confirmed,
            activated=True
        )
        user.set_passphrase(form.passphrase.data)
        with session_scope() as session:
            session.add(user)
            session.flush()
            login_user(user)
        return redirect(url_for('.dashboard'))

    return render_template('signup.jinja', form=form)


@blueprint.route('/dashboard/')
@login_required
def dashboard():
    return render_template('dashboard.jinja')


@blueprint.route('/logout/')
def logout():
    """
    Logs the user out and redirects them back to the login page
    """
    logout_user()

    return redirect(url_for('.login'))
