from flask.ext.debugtoolbar import DebugToolbarExtension

def configure_toolbar(app):
    DebugToolbarExtension(app)
