from __future__ import print_function
# py3 print function for test purposes
import sys
import os
import argparse
# importing these so we can patch them in the tests
from __builtin__ import raw_input, print
from jinja2 import Environment, FileSystemLoader
from sqlalchemy.exc import IntegrityError
from itsdangerous import URLSafeSerializer
from searchology.db import session_scope
from searchology.db.models import Users, BetaUsers


class Main(object):

    def __init__(self, args):
        self.email = args.email
        self.serializer = URLSafeSerializer(
            os.environ.get(
                'ITSDANGEROUS_SECRET_KEY', 'test-secret'))
        self.jinja_env = Environment(loader=FileSystemLoader(
            os.path.join(os.path.dirname(__file__), 'templates')
        ))
        self.template = self.jinja_env.get_template('activation_email.txt')

    def __call__(self):

        if self.existing_user_is_activated:
            raise Exception(
                '{} exists and has already been activated.'.format(
                    self.email))

        if self.existing_user_has_email:
            choices = '(y/n)'
            answer = raw_input(
                'there is already a user with that email. would '
                'you like to continue? {}'.format(choices))
            if not self.valid_choice(answer):
                sys.exit()

        self.add_beta_user()

        print(self.template.render({
            'activation_link': self.serialized_email
        }))

    @property
    def serialized_email(self):
        return self.serializer.dumps(self.email)

    def add_beta_user(self):
        beta_user = BetaUsers(
            email=self.email
        )
        try:
            with session_scope() as session:
                session.add(beta_user)
        except IntegrityError:
            print('email exists in beta_users table already...')

    def valid_choice(self, choice):
        return choice in ['y', 'Y', 'yes']

    @property
    def user(self):
        if not hasattr(self, '_user'):
            with session_scope() as session:
                self._user = session.query(
                    Users).filter_by(
                        email=self.email).first()
                session.expunge_all()
        return self._user

    @property
    def existing_user_has_email(self):
        return False if self.user is None else True

    @property
    def existing_user_is_activated(self):
        if self.user is not None and self.user.activated:
            return True
        return False


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--email', type=str, required=True)
    args = parser.parse_args()
    main = Main(args)
    main()
