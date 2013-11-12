from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
import os

engine = create_engine(
    os.environ.get(
        'SQLALCHEMY_DATABASE_URI', 'postgresql://@/searchology'))
Session = scoped_session(sessionmaker(bind=engine))


@contextmanager
def session_scope():
    """
    Provide a transactional scope around a series of operations.

    **Usage:**

    .. code-block:: python
        from searchology.db import session_scope
        with session_scope as session:
            objs = session.query(SomeModel).all()
        # do something with objs
    """

    session = Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()
