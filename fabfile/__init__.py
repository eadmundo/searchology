from fabric.api import task
from fabric.colors import cyan
#from fabric.context_managers import settings

from fabfile.utils import do
from fabfile.venv import venv_path

# Fabfile modules
import venv
import puppet
# import db


@task
def build(make=True):
    """
    Execute build tasks.
    """
    venv.build(venv_path=venv_path)
    # db.build()
    # db.populate()


@task
def test(tests='', with_blockage=False):
    """
    Run tests.
    """
    print(cyan('Running tests...'))
    print ' --with-blockage' if with_blockage else ''
    do(
        'export SOMA_ENVIRONMENT=test && {}/bin/nosetests'
        ' --nologcapture --exclude-dir-file=\'.noseexclude\''
        ' --with-yanc --with-specplugin -q --nocapture{}'
        ' {}'.format(
            venv_path,
            ' --with-blockage' if with_blockage else '',
            tests
        )
    )


@task
def coverage(tests=''):
    """
    Run tests.
    """
    print(cyan('\nRunning tests...'))
    do(
        'export SOMA_ENVIRONMENT=test && {}/bin/nosetests'
        ' --exclude-dir-file=\'.noseexclude\' --with-coverage '
        '--cover-package=daemon --cover-package=service'
        ' {}'.format(
            venv_path,
            tests
        )
    )


@task
def run():
    """
    Run the app on a development server
    """
    print(cyan('\nRunning development server...'))


@task
def shell():
    """
    Run a shell with development settings
    """
    print(cyan('\nRunning development shell...'))
