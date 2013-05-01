"""
fabfile module containing Puppet-related tasks.
"""
from fabric.decorators import task
from fabric.colors import cyan
from fabfile.utils import do
from fabric.api import settings


@task
def test():
    """Puppet noop for smoke testing."""
    print(cyan('\nRunning puppet noop'))
    do(
        'sudo /usr/bin/puppet apply --noop '
        '--modulepath="puppet/modules" "puppet/manifests/site.pp"')


@task
def check():
    """Syntax check on Puppet config."""
    print(cyan('\nChecking puppet syntax...'))
    do('find puppet -type f -name \'*.pp\' |xargs puppet parser validate')


@task
def run():
    """Apply Puppet manifest."""
    with settings(warn_only=True):
        check()
    print(cyan('\nApplying puppet manifest...'))
    do('sudo /usr/bin/puppet apply --modulepath="puppet/modules" "puppet/manifests/site.pp"')
