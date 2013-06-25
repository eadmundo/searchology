from flask.ext.login import LoginManager, current_user

from db.models import Users

login_manager = LoginManager()
login_manager.login_view = 'users.login'


@login_manager.user_loader
def load_user(user_id):
    try:
        return Users.query.get(int(user_id))
    except:
        return None
