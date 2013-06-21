# -*- mode: ruby -*-
# vi: set ft=ruby :

$script = <<SCRIPT
cd /vagrant && virtualenv --system-site-packages env
pip install -r requirements.txt
SCRIPT

Vagrant.configure("2") do |config|

  config.vm.box = "precise64"

  config.vm.box_url = "http://files.vagrantup.com/precise64.box"

  config.vm.network :private_network, ip: "173.16.1.2"
  config.vm.network :forwarded_port, guest: 8080, host: 8080
  config.vm.network :forwarded_port, guest: 9200, host: 9200
  config.vm.network :forwarded_port, guest: 5001, host: 5001
  config.vm.synced_folder ".", "/vagrant", :nfs => true

  # Puppet bootstrap - update apt cache
  config.vm.provision :puppet do |puppet|
    puppet.manifests_path = "puppet/manifests"
    puppet.module_path = "puppet/modules"
    puppet.manifest_file  = "bootstrap/apt-update.pp"
  end

  # Puppet bootstrap - build essentials
  config.vm.provision :puppet do |puppet|
    puppet.manifests_path = "puppet/manifests"
    puppet.module_path = "puppet/modules"
    puppet.manifest_file  = "bootstrap/build-essentials.pp"
  end

    # Puppet bootstrap - install augeas
  config.vm.provision :puppet do |puppet|
    puppet.manifests_path = "puppet/manifests"
    puppet.module_path = "puppet/modules"
    puppet.manifest_file  = "bootstrap/vagrant-puppet.pp"
  end

  # Puppet stand alone.
  config.vm.provision :puppet do |puppet|
    puppet.manifests_path = "puppet/manifests"
    puppet.module_path = "puppet/modules"
    puppet.manifest_file  = "site.pp"
  end

  #config.vm.provision :shell, :inline => $script

end
