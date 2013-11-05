class nginx {
  package { 'nginx':
    ensure => 'installed',
  }
  # Disable default nginx site
  file { '/etc/nginx/sites-enabled/default':
    ensure => 'absent',
    before => Service['nginx']
  }
  service { 'nginx':
    ensure => 'running',
  }
}

class nginx::site::docs() {
  file { "/etc/nginx/sites-enabled/django-docs":
    ensure  => present,
    owner   => root,
    group   => root,
    mode    => '644',
    content => template("nginx/sites-enabled/django-docs.tpl"),
    require => Package['nginx'],
    notify  => Service['nginx'],
  }
}