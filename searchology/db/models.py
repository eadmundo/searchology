import bcrypt
from sqlalchemy import (Column, Integer, String, ForeignKey)
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True, nullable=False)
    passphrase_hash = Column(String(60), nullable=False)
    # domains = relationship('SiteSearch', backref='users')

    def __repr__(self):
        return '<User %r>' % self.username

    def __init__(self, **data):

        for key, value in data.items():
            setattr(self, key, value)

    def get_passphrase(self):
        return "I'm afraid I can't do that for you, Dave"

    def set_passphrase(self, plaintext):
        # TODO: should the work rate be configurable?
        self.passphrase_hash = bcrypt.hashpw(plaintext, bcrypt.gensalt())

    passphrase = property(get_passphrase, set_passphrase)

    def is_active(self):
        """
        Flask-Login helper.
        """
        return self.enabled

    def is_authenticated(self):
        """
        Flask-Login helper.
        """
        return True

    def is_anonymous(self):
        """
        Flask-Login helper.
        """
        return False

    def get_id(self):
        """
        Flask-Login helper. Token used in the user's session to store/retrieve
        the user object.
        """
        return unicode(int(self.id))

    @classmethod
    def login(cls, username, passphrase):
        "If the credentials match, return a user record"
        user = cls.query.filter_by(username=username).first()
        matches = lambda pw, hash: hash and bcrypt.hashpw(pw, hash) == hash
        if user and matches(passphrase, user.passphrase_hash):
            return user
        return None


class SiteSearch(Base):
    __tablename__ = 'site_search'
    id = Column(Integer, primary_key=True)
    domain = Column(String, ForeignKey('users.domains'), nullable=False)
