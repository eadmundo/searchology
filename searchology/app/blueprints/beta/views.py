from flask import render_template
from searchology.app.blueprints.beta import blueprint


@blueprint.route('/')
def beta_home():
    """"
    The beta home page
    """
    return render_template('beta.jinja')
