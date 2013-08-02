from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
import os

engine = create_engine(
    os.environ.get(
        'SQLALCHEMY_DATABASE_URI', 'postgresql://@/searchology'))
Session = scoped_session(sessionmaker(bind=engine))
session = Session()
