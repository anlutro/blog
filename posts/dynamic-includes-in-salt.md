# Dynamic includes in Salt
pubdate: 2016-03-29 20:28:06 +0200
tags: Salt

Writing Salt state files can be somewhat deceptive. They have a concept of
includes, which allows you to split up state files and define dependencies,
which can give you reduced duplication, a cleaner top.sls and a way to run state
files individually without dropping all your requirements. However, unlike
Python and other programming languages, the includes don't need (it's not even
considered best practice) to be defined at the top of the file. Realizing this
opens some opportunities.

For example, consider a state file `uwsgi/apps.sls` that sets up various UWSGI
applications:

	include:
	  - uwsgi.install

	{% for name, app in pillar.get('uwsgi_apps', {}).items() %}
	/etc/uwsgi/{{ name }}.ini:
	  file.managed:
	    - source: salt://uwsgi/files/uwsgi.ini.jinja
	    - template: jinja
	    - context: { app: {{ app | yaml }} }
	{% endfor %}

Obviously missing from this example is how to get the source code for the UWSGI
applications, and setting up a systemd/supervisord service that keeps the app
running. Ignore that.

UWSGI apps can be of many types: Ruby, Python (both v2 and v3), Perl, you name
it. How do we deal with this? We could just include all the plugin types at the
top of the SLS:

	include:
	  - uwsgi.install
	  - uwsgi.plugins.perl
	  - uwsgi.plugins.python2
	  - uwsgi.plugins.python3
	  - uwsgi.plugins.ruby

	{% for name, app in pillar.get('uwsgi_apps', {}).items() %}
	...

But it'd be nicer if we could include the plugins dynamically, based on whether
any apps use them:

	{% set include_plugins = [] %}
	{% for name, app in pillar.get('uwsgi_apps', {}).items() %}
	  {% for plugin in app.get('plugins', []) if plugin not in include_plugins %}
		  {% do include_plugins.append(plugin) %}
	  {% endfor %}
	/etc/uwsgi/{{ name }}.ini:
	  file.managed:
	    - source: salt://uwsgi/files/uwsgi.ini.jinja
	    - template: jinja
	    - context: { app: {{ app | yaml }} }
	{% endfor %}

	include:
	  - uwsgi.install
	{% for sls in include_plugins %}
	  - uwsgi.plugin.{{ sls }}
	{% endfor %}
