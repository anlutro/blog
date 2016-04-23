# Dangers of targetting grains in Salt
subtitle: Or how to properly do role management with Salt
pubdate: 2016-03-01 23:32:09 +0100
tags: Salt

Targetting grains is probably the most widespread bad practice in Salt. It helps
reduce verbosity and duplication in your top files, but also opens up some
serious security holes in the event that a minion should be compromised.

A typical grain-focused setup would be something like this:

	# a minion's /etc/salt/grains
	roles:
	  - webserver
	  - database

	# top.sls for states and/or pillars
	base:
	  {{ grains.id }}:
	  {% for role in grains.get('roles', []) %}
	   - {{ role }}
	  {% endfor %}

If a minion gets compromised (someone gets root access who shouldn't have), that
means the grains file could be edited. Depending on your setup, this could have
various security implications.

If your pillar top file targets grains, sensitive pillar data like usernames,
passwords and private keys (even for roles unrelated to the host's real role)
would be easily obtainable. If you also use grains to determine which customer
or which cluster the host is part of, a server could gain access to other
customers'/clusters' data.

If you use the mine for basic service discovery, a compromised server could also
make other servers start trying to connect to it. For example, it could fake
itself as a RabbitMQ server, or a database server, and receive a bunch of data
that may contain sensitive information.

Worst case scenario: A compromised host is able to change itself into being a
salt master, which all your minions connect to because you use the mine as
service discovery, giving the attacker full access to all your minions.


### What to do instead?

Match on the minion ID/hostname whenever practical. A database server will
always start with "db", an application server will always start with "app", and
so on. The customer/cluster name will be another part of the minion ID, as will
the environment and datacenter of the host.

If you want to avoid duplication between state and pillar top.sls files, you can
consider rendering your state top.sls based on pillar data, like this:

	# state top.sls
	{{ grains.id }}:
	  {% for state in pillar.get('states', []) %}
	   - {{ state }}
	  {% endfor %}

As opposed to grains, this is secure, because pillar data is rendered entirely
on the master side and cannot be tampered with by the minion. 

There will be some exceptions, situations where the hostname alone simply can't
convey enough information, and you don't want to enter each individual host into
your top file. Grains can be an option here, but you need to decide whether it
can be a security risk if the grain gets changed. For example, your app servers
may run various types of web applications:

	'app* and G@app_type:php':
	  - match: compound
	  - php
	'app* and G@app_type:python':
	  - match: compound
	  - python

This is relatively safe because installing PHP instead of/in addition to Python
on an app server won't damage anything outside of the compromised host. Also,
we explicitly state which pillar/state to include, instead of blindly accepting
the grain value.

Finally, if you use an external pillar to store your data instead of the top
file structure, you automatically solve a lot of the problems you were trying to
solve by using grains in the first place. Using a relational database, for
example, means you could write a nice admin interface for managing all the
different servers, and duplication of data is no longer a big deal. You can also
do custom data processing in the external pillar python module.
