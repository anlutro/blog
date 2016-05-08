# Managing systemd units with Salt
pubdate: 2016-05-08 07:58:11 +0200
tags: Salt

In many cases, you will want to manage your own systemd service definitions.
Here's how.

	example_systemd_unit:
	  file.managed:
	    - name: /etc/systemd/system/example.service
	    - source: salt://example/systemd_unit.jinja
	    - template: jinja
	  module.run:
	    - name: service.systemctl_reload
	    - onchanges:
	      - file: example_systemd_unit

	example_running:
	  service.running:
	    - name: example
	    - watch:
	      - module: example_systemd_unit

Let's walk through what this does. First we manage the systemd unit, which is
just a file ending with `.service` in the correct directory. You may need to
change the path to `example.service` based on your Linux distribution.

Second we have a `module.run` state calling `service.systemctl_reload`, but only
when the service file changes. Systemd documentation will tell you that you need
to run `systemctl reload` to apply changes made to service files, this is simply
the Salt way of doing that.

Finally, we have a regular `service.running`. You just need to make sure the
name of the service matches the name of your `.service` file, and also make sure
that the every time the service definition changes and
`service.systemctl_reload` gets called, the service also gets restarted. A watch
is an implicit require, so we don't need to specify that the service state
requires the service file to be present.
