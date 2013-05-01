class vagrant {

  line { 'cd-vagrant':
    ensure => absent,
    file   => '/home/vagrant/.bashrc',
    line   => 'cd /vagrant',
  }

  line { 'line-venv-activate':
    ensure => present,
    file   => '/home/vagrant/.bashrc',
    line   => 'cd /vagrant && source env/bin/activate',
  }

}
