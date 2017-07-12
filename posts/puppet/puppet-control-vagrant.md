# Using a puppet-control repo in Vagrant
pubdate: 2017-07-12T11:11:43+02:00
tags: Puppet, Vagrant

Whether you use Puppet Enterprise or r10k, using a "control repo" with a branch
for every environment is the way you want to set up Puppet these days. Finding a
way to make this work well with Vagrant for local development was surprisingly
difficult - most guides out there focus on a very simple puppet setup with no
modules, or maybe assuming that puppet is installed on the host operating
system. I wanted to write a bit about the things I discovered while
experimenting trying to get a proper setup up and running.

This is not meant as an introduction to puppet or vagrant - you might want to
read up on how to use these tools before starting this article, as I won't go
into detail on how puppet or vagrant configuration works..

I'll assume you already have a puppet-control repository. If you don't, have a
look at this [template repo](https://github.com/puppetlabs/control-repo).

## Modifications to the control repo

First of all, you probably want to add .gitignore rules in your control repo for
node-specific hieradata for vagrant files, so that you can modify these files as
much as you want. If you use the default hierarchy and make sure that all your
vagrant hostnames end with `.vagrant` it would look like this:

	/hieradata/nodes/*.vagrant.yaml

Also make sure to add some sort of generic vagrant hiera file which applies to
all vagrant machines. We set a `provider` custom fact which is set to "vagrant"
for vagrant machines, and then load the hiera file
`providers/%{facts.provider}.yaml`, but if you can think of another way of
setting generic hiera data for vagrant machines, you can do it however you want.

## How we'll run Puppet

By default, r10k creates one environments for every git branch. This is rather
nice for deploying things remotely, but for developing locally, this means we'd
have to commit and run a deploy command before any change we make becomes
"public" to the Vagrant machines. This is too slow for us, so we will be using
r10k sparingly - mostly just to install modules. We could actually use puppet-
librarian instead and get module dependency management, but we'll stick with
r10k to stay consistent with our production environment.

We'll create a "fake" environment called "vagrant", which all of our VMs will
use (configured through puppet.conf). This environment will be a plain directory
on the VM's filesystem, and we'll simply invoke puppet using `puppet apply`.

## Creating the Vagrant repo

We'll create a new git repo which contains the Vagrant configuration:

- A Vagrantfile
- Provisioning scripts
- Puppet configuration
- r10k configuration

The control repo can exist inside of this vagrant repo (make sure to .gitignore
it!) or outside. The important thing here is to share the correct directories in
the Vagrantfile:

	config.vm.share './control', '/etc/puppetlabs/code/environments/vagrant'
	config.vm.share './puppet', '/etc/puppetlabs/puppet'
	config.vm.share './r10k', '/etc/puppetlabs/r10k'

## Configuration files

We do not need a lot of configuration to make this work. I'll refer to
configuration file paths relative to the directory where your Vagrantfile is.

`puppet/puppet.conf` only needs to contain "environment = vagrant". You might
want to add various configuration to stay consistent with your production
environment, of course.

`puppet/hiera.yaml` does need to be present, but does not need any actual
configuration. We need to put "version: 5" in there to prevent Puppet warnings.

`r10k/r10k.yaml` should contain "cachedir: /var/cache/r10k".

## Provisioning

While Vagrant comes with a Puppet provisioner, it does not work that well with
our workflow, so we just write a custom shell script that does the necessary
things to get everything set up. Here's an example for CentOS/RHEL:

	#!/bin/sh
	rhv=$(cat /etc/redhat-release | grep -Po '\d' | head -1)
	rpm -Uvh https://yum.puppetlabs.com/puppetlabs-release-pc1-el-${rhv}.noarch.rpm
	yum -y install puppet-agent
	/opt/puppetlabs/puppet/bin/gem install r10k

Add it to our Vagrantfile:

	config.vm.provision 'install_puppet', type: 'shell', path: 'install_puppet.sh'

Let's make sure it works by running this command:

	$ vagrant up && vagrant ssh

## Our first puppet run

We're almost ready to run puppet - only one thing is missing: Installing modules
and their dependencies. We'll do this manually with r10k, inside the virtual
machine:

	$ cd /etc/puppetlabs/code/environments/vagrant
	$ sudo /opt/puppetlabs/puppet/bin/r10k puppetfile install

You may also want to check for missing dependencies which need to be added to
your puppetfile:

	$ sudo /opt/puppetlabs/bin/puppet module list --tree

Once this is done, we can try executing a class:

	$ sudo /opt/puppetlabs/bin/puppet apply -e "include profile::base"

At this point, you can start editing and testing your code changes in puppet-
control.
