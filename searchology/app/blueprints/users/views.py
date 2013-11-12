from flask import redirect, request, url_for, flash, render_template
from flask.ext.login import current_user, login_user, logout_user
from searchology.app.blueprints.users.forms import LoginForm
from searchology.app.blueprints.users import blueprint
from searchology.app.extensions.database import database
from searchology.db.models import Users


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
            return redirect(request.args.get('next') or url_for('profiles.profile', username=user.username))
        else:
            flash('Login failed', 'error')

    return render_template('login.jinja', form=form)


@blueprint.route('/logout/')
def logout():
    """
    Logs the user out and redirects them back to the login page
    """
    logout_user()

    return redirect(url_for('.login'))
