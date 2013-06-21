class elasticsearch {

  $version = '0.20.6'
  $java_package = 'openjdk-7-jre'
  $download = "https://download.elasticsearch.org/elasticsearch/elasticsearch/elasticsearch-0.20.6.tar.gz"
  $dest = "/opt/elasticsearch-${version}"

  package { "${java_package}":
    ensure => 'installed',
  }

  group { 'elasticsearch':
    ensure => present,
    system  => true,
  }

  user { 'elasticsearch':
    ensure  => present,
    system  => true,
    home    => $dest,
    shell   => '/bin/sh',
    gid     => 'elasticsearch',
    require => Group['elasticsearch'],
  }

  exec { 'download-elasticsearch':
    user    => 'elasticsearch',
    cwd     => '/tmp',
    command => "/usr/bin/wget -q ${download} -O elasticsearch-${version}.tar.gz",
    timeout => 300,
    creates => "/tmp/elasticsearch-${version}.tar.gz"
  }

  exec { 'extract-elasticsearch':
    user    => 'elasticsearch',
    cwd     => '/tmp',
    command => "/bin/tar xzf /tmp/elasticsearch-${version}.tar.gz",
    creates => "/tmp/elasticsearch-${version}",
    require => Exec[download-elasticsearch]
  }

  exec { "elasticsearch-${version}":
    command => "/bin/mv /tmp/elasticsearch-${version} ${dest}",
    cwd     => "/tmp",
    creates => $dest,
    require => Exec[extract-elasticsearch],
  }

  file { '/usr/bin/elasticsearch':
    ensure  => link,
    target  => "${dest}/bin/elasticsearch",
    require => Exec["elasticsearch-${version}"],
  }

  file { '/var/lib/elasticsearch':
    ensure  => directory,
    owner   => 'elasticsearch',
    group   => 'elasticsearch',
    mode    => '0755',
    require => User['elasticsearch'],
  }

  file { "${dest}/logs":
    ensure  => directory,
    owner   => 'elasticsearch',
    group   => 'elasticsearch',
    mode    => '0755',
    require => User['elasticsearch'],
  }

  file { "${dest}/config/elasticsearch.yml":
    ensure  => present,
    content => template("elasticsearch/elasticsearch.yml"),
    owner => elasticsearch,
    group => elasticsearch,
    require => Exec["elasticsearch-${version}"]
  }

  file { "${dest}/config/logging.yml":
    ensure  => present,
    content => template("elasticsearch/logging.yml"),
    owner => elasticsearch,
    group => elasticsearch,
    require => Exec["elasticsearch-${version}"]
  }

  file { "${dest}/config/stopwords.txt":
    ensure  => present,
    content => template("elasticsearch/stopwords.txt"),
    owner => elasticsearch,
    group => elasticsearch,
    require => Exec["elasticsearch-${version}"]
  }

  file { "/etc/circus.d/elasticsearch.ini":
    ensure => present,
    content => template("elasticsearch/circus.ini"),
    require => [File["/etc/circus.d"], Exec["elasticsearch-${version}"]],
    notify => Service[circus],
  }

  file { "${dest}/config/work":
    ensure => directory,
    owner => elasticsearch,
    group => elasticsearch,
    require => Exec["elasticsearch-${version}"]
  }

  file { "${dest}/config/templates":
    ensure => directory,
    owner => elasticsearch,
    group => elasticsearch,
    require => Exec["elasticsearch-${version}"]
  }

  file { "${dest}/config/templates/index_template.json":
    ensure => present,
    content => template('elasticsearch/index_template.json'),
  }

  line { 'line-elasticsearch-soft-limit':
    ensure => present,
    file   => '/etc/security/limits.conf',
    line   => 'elasticsearch soft nofile 32000',
  }

  line { 'line-elasticsearch-hard-limit':
    ensure => present,
    file   => '/etc/security/limits.conf',
    line   => 'elasticsearch hard nofile 32000',
  }

  exec { 'plugin-head':
    command => "${dest}/bin/plugin -install mobz/elasticsearch-head",
    require => [Exec["elasticsearch-${version}"], Package["$java_package"], File["/etc/circus.d/elasticsearch.ini"]],
    creates => "${dest}/plugins/head",
  }

  exec { 'plugin-bigdesk':
    command => "${dest}/bin/plugin -install lukas-vlcek/bigdesk",
    require => [Exec["elasticsearch-${version}"], Package["$java_package"], File["/etc/circus.d/elasticsearch.ini"]],
    creates => "${dest}/plugins/bigdesk",
  }

  exec { 'plugin-aws':
    command => "${dest}/bin/plugin -install elasticsearch/elasticsearch-cloud-aws/1.9.0",
    require => [Exec["elasticsearch-${version}"], Package["$java_package"], File["/etc/circus.d/elasticsearch.ini"]],
    creates => "${dest}/plugins/cloud-aws",
  }

}
