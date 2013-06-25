import os
from flask import Flask
from app.extensions.database import database
from app.extensions.toolbar import configure_toolbar
from app.extensions.login import login_manager, current_user
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
        module = __import__('app.blueprints.%s.views' % blueprint[0], globals(), locals(), '*')
        app.register_blueprint(module.blueprint, url_prefix=blueprint[1])


def create_app(config=None, blueprints=None):
    """
    Create and initialise the application.
    """
    app = Flask(__name__)
    app.config.from_pyfile('%s/config/default.py' % app.root_path)

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
