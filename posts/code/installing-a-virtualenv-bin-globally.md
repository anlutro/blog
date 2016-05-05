# Installing a virtualenv bin globally
pubdate: 2015-10-10 09:54:43 +0100
tags: Python, Virtualenv

TLDR: Symlink `/path/to/virtualenv/bin/my-script` to `~/bin/my-script`

Sometimes you want to install a python script with dependencies. However, those dependencies might clash with other python script's dependencies, or you may just not want to clutter the system with packages installed with package managers that aren't your system's native one.

Virtualenvs are usually a good way to deal with this, but you have to manually activate the virtualenv before running your script. Or do you?

Interestingly, python seems to look for packages/includes/whatever relative to the path of the python binary. If we run a python script with `/usr/bin/python`, the virtualenv's packages won't be pulled in, but if we run it with `/path/to/virtualenv/bin/python`, they will.

	$ /usr/bin/python ./bin/salt --version
	[ ... ]
	ValueError: Expected version spec in [ ... ]
	$ ./bin/python ./bin/salt --version
	salt 2015.8.0-154-g4a69db2 (Beryllium)

If we look at the shebang line of a script file in our virtualenv's `bin` directory, we can see that it specifies the absolute path to the python bin file in our virtualenv:

	$ head -1 bin/salt
	#!/home/andreas/dev/python/salt/bin/python2

This means that we can simply symlink the script to `~/bin` or `/usr/local/bin` and it'll work, even if the virtualenv isn't activated.

	$ ln -s ~/dev/python/salt/bin/salt ~/bin/salt
	$ which salt
	/home/andreas/bin/salt
	$ salt --version
	salt 2015.8.0-154-g4a69db2 (Beryllium)
