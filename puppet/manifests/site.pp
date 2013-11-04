import 'lib/*.pp'
import 'nodes/*.pp'

#
# Modules included for all nodes.
#
class common {

    include python
    include git
    include fabric
    include curl
    include circus
    include zeromq
    include jdk
    include jpype
    include libxml2
    include libxslt
    include postgresql-dev
    include postgresql
    include elasticsearch
    include redis

    # create the database
    postgresql::database { 'searchology':
      ensure => present,
    }

    # create the vagrant role
    postgresql::role { 'vagrant':
      ensure => present,
    }

}
