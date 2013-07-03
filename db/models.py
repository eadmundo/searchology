import bcrypt
from sqlalchemy import (Column, Integer, String, Unicode, ForeignKey, UnicodeText, Boolean, DateTime)
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
import db


Base = declarative_base()


class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True, nullable=False)
    passphrase_hash = Column(String(60), nullable=False)
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
    domain = Column(String, nullable=False)


class Client(Base):
    __tablename__ = 'client'
    # human readable name, not required
    name = Column(Unicode(40))

    # human readable description, not required
    description = Column(Unicode(400))

    # creator of the client, not required
    user_id = Column(ForeignKey('users.id'))
    # required if you need to support client credential
    user = relationship('Users')

    client_id = Column(Unicode(40), primary_key=True)
    client_secret = Column(Unicode(55), unique=True, index=True, nullable=False)

    # public or confidential
    is_confidential = Column(Boolean)

    _redirect_uris = Column(UnicodeText)
    _default_scopes = Column(UnicodeText)

    @property
    def client_type(self):
        if self.is_confidential:
            return 'confidential'
        return 'public'

    @property
    def redirect_uris(self):
        if self._redirect_uris:
            return self._redirect_uris.split()
        return []

    @property
    def default_redirect_uri(self):
        return self.redirect_uris[0]

    @property
    def default_scopes(self):
        if self._default_scopes:
            return self._default_scopes.split()
        return []


class Grant(Base):
    __tablename__ = 'grant'
    id = Column(Integer, primary_key=True)

    user_id = Column(
        Integer, ForeignKey('user.id', ondelete='CASCADE')
    )
    user = relationship('User')

    client_id = Column(
        Unicode(40), ForeignKey('client.client_id'), nullable=False,
    )
    client = relationship('Client')

    code = Column(Unicode(255), index=True, nullable=False)

    redirect_uri = Column(Unicode(255))
    expires = Column(DateTime)

    _scopes = Column(UnicodeText)

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return self

    @property
    def scopes(self):
        if self._scopes:
            return self._scopes.split()
        return []


class Token(Base):
    __tablename__ = 'token'
    id = Column(Integer, primary_key=True)
    client_id = Column(
        Unicode(40), ForeignKey('client.client_id'), nullable=False,
    )
    client = relationship('Client')

    user_id = Column(
        Integer, ForeignKey('user.id')
    )
    user = relationship('User')

    # currently only bearer is supported
    token_type = Column(Unicode(40))

    access_token = Column(Unicode(255), unique=True)
    refresh_token = Column(Unicode(255), unique=True)
    expires = Column(db.DateTime)
    _scopes = db.Column(db.UnicodeText)

    @property
    def scopes(self):
        if self._scopes:
            return self._scopes.split()
        return []
