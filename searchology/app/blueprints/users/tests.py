import unittest
import factory
from searchology.db import session_scope, engine
from searchology.db.models import Users, BetaUsers, Base
from searchology.app.blueprints.users.views import get_user_with_beta_email


class UsersFactory(factory.Factory):
    FACTORY_FOR = Users
    beta_id = 1


class BetaUsersFactory(factory.Factory):
    FACTORY_FOR = BetaUsers
    email = 'beta@email.com'


class TestUsersBlueprint(unittest.TestCase):

    def setUp(self):
        Base.metadata.create_all(engine)
        user = UsersFactory.create()
        beta_user = BetaUsersFactory.create()
        with session_scope() as session:
            session.add(user)
            session.add(beta_user)

    def tearDown(self):
        Base.metadata.drop_all(engine)

    def test_get_user_with_beta_email(self):
        self.assertEqual(
            get_user_with_beta_email('beta@email.com').id,
            1
        )

if __name__ == "__main__":
    unittest.main()
