from searchology.app import create_app
from flask import current_app
from flask.ext.script import Shell, Manager, Server

manager = Manager(create_app)


def _make_shell_context():
    """
    Shell context: import helper objects here.
    """
    from searchology.app.extensions.db import db
    return dict(app=current_app, db=db)


manager.add_option('--flask-config', dest='config', help='Specify Flask config file', required=False)
manager.add_command('shell', Shell(make_context=_make_shell_context))
manager.add_command('runserver', Server(host='0.0.0.0', port=5001))

if __name__ == "__main__":
    manager.run()
