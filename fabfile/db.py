"""
fabfile module for managing database-related tasks.
"""
from fabric.api import task
from fabric.utils import abort
from fabric.context_managers import settings, hide
from fabric.colors import cyan
from fabfile.utils import do
from fabfile.venv import venv_path

from sqlalchemy import create_engine
#from socialgraph.models import Base


@task
def build():
    """Initialise and migrate database to latest version."""
    print(cyan('\nUpdating database...'))

    # Ensure database exists
    if not _pg_db_exists(DB['name']):
        do('createdb -O \'%(user)s\' \'%(name)s\'' % DB)

    # Ensure indexer has permission on all objects
    do('psql -tAc \'GRANT ALL ON ALL TABLES IN SCHEMA public TO "%(user)s";\' %(name)s' % DB)
    do('psql -tAc \'GRANT ALL ON ALL SEQUENCES IN SCHEMA public TO "%(user)s";\' %(name)s' % DB)
    do('psql -tAc \'ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO GROUP "%(user)s";\' %(name)s' % DB)
    do('psql -tAc \'ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO GROUP "%(user)s";\' %(name)s' % DB)

    print(cyan('\nCreating tables...'))
    engine = create_engine('postgresql://@/socialgraph')
    Base.metadata.create_all(engine)


def _pg_db_exists(database):
    """
    Helper function to check if the postgresql database exists.
    """
    with settings(hide('running', 'warnings'), warn_only=True):
        return do('psql -tAc "SELECT 1 FROM pg_database WHERE datname = \'%s\'" postgres |grep -q 1' % database, capture=True).succeeded
