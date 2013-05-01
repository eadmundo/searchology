class postgresql-dev {
  package { ['libpq-dev']:
    ensure => present,
  }
}