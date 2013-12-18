import bcrypt
from sqlalchemy import (Column, Integer, String, ForeignKey, Boolean, DateTime)
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime


Base = declarative_base()


class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    email_confirmed = Column(Boolean, default=False)
    passphrase_hash = Column(String(60), nullable=False)
    activated = Column(Boolean, default=False)
    date_activated = Column(DateTime, nullable=False, default=datetime.now())
    domains = relationship('SiteSearch', backref='users')

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
        return self.activated

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

    def passphrase_matches(self, passphrase):
        matches = lambda pw, hash: hash and bcrypt.hashpw(pw, hash) == hash
        return matches(passphrase, self.passphrase_hash)


class SiteSearch(Base):
    __tablename__ = 'site_search'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    domain = Column(String(255), nullable=False)


class BetaUsers(Base):
    __tablename__ = 'Beta_users'
    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True, nullable=False)
    activated = Column(Boolean, default=False)
    date_activated = Column(
        DateTime, nullable=True)

    def __init__(self, **data):
        for key, value in data.items():
            setattr(self, key, value)
