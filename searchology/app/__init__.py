import os
from flask import Flask
from searchology.app.extensions.database import database
from searchology.app.extensions.toolbar import configure_toolbar
from searchology.app.extensions.login import login_manager, current_user
from searchology.app.extensions.oauth import oauth
# from app.helpers import Pagination


DEFAULT_BLUEPRINTS = [
    ('beta', ''),
    ('api', '/api'),
    ('users', ''),
    # ('profiles', ''),
]


def configure_extensions(app):
    """
    Set up Flask extensions.
    """
    database.init_app(app)
    login_manager.init_app(app)
    configure_toolbar(app)
    oauth.init_app(app)
    # principal.init_app(app)


def configure_context_processors(app):

    @app.context_processor
    def current_user_context():
        "Puts the currently logged-in user into the context as `current_user`"
        return dict(current_user=current_user)

    @app.context_processor
    def debug(debug=app.debug):
        """
        Notify templates that they're in debug mode
        """
        return dict(debug=debug)


def configure_blueprints(app, blueprints):
    """
    Register blueprints.
    """
    for blueprint in blueprints:
        # Import blueprint from view module
        module = __import__('searchology.app.blueprints.%s.views' % blueprint[0], globals(), locals(), '*')
        app.register_blueprint(module.blueprint, url_prefix=blueprint[1])


def create_app(config=None, blueprints=None):
    """
    Create and initialise the application.
    """
    app = Flask(__name__)
    app.config.from_pyfile('%s/config/default.py' % app.root_path)

    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
        'SQLALCHEMY_DATABASE_URI', 'postgresql://@/searchology')

    if config:
        app.config.from_pyfile(config)
    elif os.getenv('FLASK_CONFIG'):
        app.config.from_envvar('FLASK_CONFIG')

    if blueprints is None:
        blueprints = DEFAULT_BLUEPRINTS

    configure_extensions(app)
    configure_context_processors(app)
    configure_blueprints(app, blueprints)

    return app


# @app.route('/')
# def results():
#     page = int(request.args.get('page', 1))
#     qstr = request.args.get('q', '')
#     count = request.args.get('count', 10)
#     results = search_results('docs.djangoproject.dev', qstr, count, page)
#     pagination = Pagination(page, count, results['hits']['total'], results['hits']['hits'])
#     return render_template('srp.jinja', pagination=pagination, qstr=qstr)
