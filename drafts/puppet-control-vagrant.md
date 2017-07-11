# Using a puppet-control repo in Vagrant
pubdate: 2017-07-11T20:49:19+02:00
tags: puppet

Whether you use Puppet Enterprise or r10k, using a "control repo" with a branch
for every environment is the way you want to set up Puppet these days. Finding a
way to make this work well with Vagrant for local development was surprisingly
difficult - most guides out there focus on a very simple puppet setup with no
modules, or maybe assuming that puppet is installed on the host operating
system. I wanted to write a bit about the things I discovered while
experimenting trying to get a proper setup up and running.

## Modifications to the control repo

First of all, you probably want to add .gitignore rules in your control repo for
node-specific hieradata for vagrant files, so that you can modify these files as
much as you want. If you use the default hierarchy and make sure that all your
vagrant hostnames end with `.vagrant` it would look like this:

	/hieradata/nodes/*.vagrant.yaml

Also make sure to add some sort of generic vagrant hiera file which applies to
all vagrant machines. We set a `provider` custom fact which is set to "vagrant"
for vagrant machines, and then load the hiera file
`providers/%{facts.provider}.yaml`, but you can do it in a lot of different
ways.

## How we'll run Puppet

By default, r10k creates one enviropetnment for every git branch. This is rather
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

We'll create a new repo which contains the Vagrant configuration:

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

We do not need a lot of configuration to make this work. `puppet.conf` can
literally be empty except from setting `environment=vagrant`. You might want to
add various configuration to stay consistent with your production environment,
of course.

## Provisioning

While Vagrant comes with a Puppet provisioner, it does not work that well with
our workflow, so we just write a custom shell script that does the necessary
things to get everything set up. Here's an example for CentOS/RHEL:

	# shell script here

Add it to our Vagrantfile:

	# vagrantfile here

## Our first puppet run

We're almost ready to run puppet - only one thing is missing: Installing modules and their dependencies. We'll do this manually with r10k:

	$ cd /etc/puppetlabs/code/environments/vagrant
	$ sudo /opt/puppetlabs/puppet/bin/r10k puppetfile install

You may also want to check for missing dependencies:

	$ sudo /opt/puppetlabs/bin/puppet module list --tree

Once this is done, we can try executing a class:

	$ sudo /opt/puppetlabs/bin/puppet apply -e "include profile::base"
