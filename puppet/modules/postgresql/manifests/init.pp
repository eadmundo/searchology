class postgresql {
  # postgresql-dev required for Python's psycopg2
  package { [ 'postgresql', 'postgresql-server-dev-all' ]:
    ensure => 'installed',
  }
  service { 'postgresql':
    ensure  => running,
    require => Package[postgresql],
  }
}

#
# TODO: Clean up! This is messy...
#
define postgresql::role( $ensure = 'present', $createdb = false, $createrole = false, $superuser = false, $grant = false ) {
  case $ensure {
    present: {

      if $createdb { $createdb_param = '-d' } else { $createdb_param = '-D' }
      if $createrole { $createrole_param = '-r' } else { $createrole_param = '-R' }
      if $superuser { $superuser_param = '-s' } else { $superuser_param = '-S' }

      exec { "/usr/bin/createuser ${createdb_param} ${createrole_param} ${superuser_param} \"$name\"":
        user    => postgres,
        unless  => "/usr/bin/psql -tAc \"SELECT 1 FROM pg_roles WHERE rolname = \'$name\'\" |grep -q 1",
        require => Service[postgresql],
      }
      if ( $grant != false ) {
        exec { "/usr/bin/psql -c \'GRANT \"$grant\" TO \"$name\";\'":
          user   => postgres,
          unless => "/usr/bin/psql -tAc \"SELECT 1 FROM pg_authid p INNER JOIN pg_auth_members am ON (p.oid = am.roleid) INNER JOIN pg_authid m ON (am.member = m.oid) INNER JOIN pg_authid g ON (am.grantor = g.oid) WHERE p.rolname = '$grant' AND m.rolname = '$name';\" |grep -q 1",
          require => [Service[postgresql], Exec["/usr/bin/createuser ${createdb_param} ${createrole_param} ${superuser_param} \"$name\""]],
        }
      }
    }
    absent: {
      exec { "/usr/bin/dropuser \"$name\"":
        user   => postgres,
        onlyif => "/usr/bin/psql -tAc \"SELECT 1 FROM pg_roles WHERE rolname = \'$name\'\" |grep -q 1",
        require => Service[postgresql],
      }
    }
  }
}

define postgresql::database( $ensure = 'present', $owner = 'postgres' ) {
  case $ensure {
    present: {
      exec { "/usr/bin/createdb -O \"$owner\" \"$name\"":
        user   => postgres,
        unless => "/usr/bin/psql -tAc \"SELECT 1 FROM pg_database WHERE datname = \'$name\'\" |grep -q 1",
        require => Service[postgresql],
      }
    }
    absent: {
      exec { "/usr/bin/dropdb \"$name\"":
        user   => postgres,
        onlyif => "/usr/bin/psql -tAc \"SELECT 1 FROM pg_database WHERE datname = \'$name\'\" |grep -q 1",
        require => Service[postgresql],
      }
    }
  }
}
