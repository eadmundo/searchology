from app.blueprints.beta import blueprint


@blueprint.route('/')
def beta_home():
    """"
    The beta home page
    """
    return 'this is just the beta home page'
