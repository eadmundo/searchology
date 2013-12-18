from flask.ext.login import LoginManager, current_user

from searchology.db.models import Users
from searchology.db import session_scope

login_manager = LoginManager()
login_manager.login_view = 'users.login'


@login_manager.user_loader
def load_user(user_id):
    with session_scope() as session:
        user = session.query(Users).filter_by(id=int(user_id)).first()
        session.expunge_all()
    return user
