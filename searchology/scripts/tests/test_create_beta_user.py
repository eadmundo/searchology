import unittest
import argparse
import factory
import fudge
from flask import url_for
from itsdangerous import URLSafeSerializer
from searchology.db import session_scope, engine
from searchology.db.models import Users, BetaUsers, Base
from searchology.scripts.create_beta_user import Main
from searchology.app import create_app


class UsersFactory(factory.Factory):
    FACTORY_FOR = Users
    username = 'existing'
    email = 'existing@email.com'
    activated = True


class BetaUsersFactory(factory.Factory):
    FACTORY_FOR = BetaUsers
    email = 'different@email.com'


class TestCreateBetaUser(unittest.TestCase):

    def setUp(self):
        self.serializer = URLSafeSerializer('test-secret')
        Base.metadata.create_all(engine)
        active_user = UsersFactory.create()
        active_user.set_passphrase('test')
        inactive_user = UsersFactory.create(
            username='different',
            email='different@email.com',
            activated=False
        )
        inactive_user.set_passphrase('test')
        with session_scope() as session:
            session.add(active_user)
            session.add(inactive_user)
        self.parser = argparse.ArgumentParser()
        self.parser.add_argument('--email', type=str)
        self.app = create_app()

    def tearDown(self):
        Base.metadata.drop_all(engine)

    def _get_main(self, args):
        return Main(self.parser.parse_args(args))

    def test_existing_user_has_email_with_existing_email(self):
        m = self._get_main(['--email', 'existing@email.com'])
        self.assertTrue(m.existing_user_has_email)

    def test_existing_user_has_email_with_new_email(self):
        m = self._get_main(['--email', 'new@email.com'])
        self.assertFalse(m.existing_user_has_email)

    def test_existing_active_user_is_activated(self):
        m = self._get_main(['--email', 'existing@email.com'])
        self.assertTrue(m.existing_user_is_activated)

    def test_existing_inactive_user_isnt_activated(self):
        m = self._get_main(['--email', 'different@email.com'])
        self.assertFalse(m.existing_user_is_activated)

    @fudge.patch('searchology.scripts.create_beta_user.raw_input')
    @fudge.patch('searchology.scripts.create_beta_user.print')
    def test_existing_inactive_user_can_have_new_activation_link(self, builtin_raw_input, print_function):
        beta_user = BetaUsersFactory.create()
        with session_scope() as session:
            session.add(beta_user)
        email = 'different@email.com'
        with self.app.test_request_context():
            url = url_for('users.login', _external=True)
        (builtin_raw_input
            .expects_call()
            .returns('y'))
        text = """Hi,

You've been invited to join the searcholo.gy beta - click the link below to try it out:

{}

Thanks!""".format('{}{}'.format(url, self.serializer.dumps(email)))
        (print_function
            .expects_call()
            .with_args('email exists in beta_users table already...')
            .next_call()
            .with_args(text))
        m = self._get_main(['--email', email])
        m()

    def test_existing_active_user_raises_exception(self):
        with self.assertRaises(Exception):
            m = self._get_main(['--email', 'existing@email.com'])
            m()

    @fudge.patch('searchology.scripts.create_beta_user.raw_input')
    @fudge.patch('searchology.scripts.create_beta_user.print')
    def test_ask_to_continue_if_email_exists_already_in_database(self, builtin_raw_input, print_function):
        (builtin_raw_input
            .expects_call()
            .returns('y'))
        (print_function
            .is_callable())
        m = self._get_main(['--email', 'different@email.com'])
        m()

    @fudge.patch('searchology.scripts.create_beta_user.raw_input')
    def test_dont_continue_if_user_doesnt_say_yes(self, builtin_raw_input):
        (builtin_raw_input
            .expects_call()
            .returns('n'))
        with self.assertRaises(SystemExit):
            m = self._get_main(['--email', 'different@email.com'])
            m()

    def test_add_beta_user(self):
        m = self._get_main(['--email', 'new@email.com'])
        m.add_beta_user()
        with session_scope() as session:
            self.assertEqual(
                session.query(BetaUsers.email).one().email,
                'new@email.com'
            )

    @fudge.patch('searchology.scripts.create_beta_user.print')
    def test_check_email_is_added_if_it_doesnt_exist(self, print_function):
        (print_function
            .expects_call())
        m = self._get_main(['--email', 'new@email.com'])
        m.add_beta_user = fudge.Fake(
            'add_beta_user'
        ).expects_call()
        m()

    def test_email_can_be_serialized_and_deserialized(self):
        m = self._get_main(['--email', 'new@email.com'])
        self.assertEqual(
            self.serializer.loads(m.serialized_email),
            'new@email.com'
        )

    @fudge.patch('searchology.scripts.create_beta_user.print')
    def test_email_text_is_output_correctly(self, print_function):
        m = self._get_main(['--email', 'new@email.com'])
        with self.app.test_request_context():
            url = url_for('beta.activate', _external=True)
        text = """Hi,

You've been invited to join the searcholo.gy beta - click the link below to try it out:

{}

Thanks!""".format('{}{}'.format(url, self.serializer.dumps('new@email.com')))
        (print_function
            .expects_call()
            .with_args(text))
        m()
