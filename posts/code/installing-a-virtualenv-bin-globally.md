# Installing a virtualenv bin globally
pubdate: 2015-10-10 09:54:43 +0100
tags: Python

TLDR: Symlink `/path/to/virtualenv/bin/my-script` to a directory in your `$PATH`, such as `~/.local/bin/my-script`

Sometimes you want to install a python script so you can run it anywhere, but it has dependencies, so you can't just download it and run it as-is. While `pip install`ing technically does *work*, the script's dependencies might clash with other python script's dependencies, or you may just not want to clutter the system with packages installed with package managers that aren't your system's native one.

Virtualenvs are usually a good way to deal with this, but you have to manually activate the virtualenv before running your script. Or do you?

Interestingly, python seems to look for packages/includes/whatever relative to the path of the python binary. If we run a python script with `/usr/bin/python`, the virtualenv's packages won't be pulled in, but if we run it with `/path/to/virtualenv/bin/python`, they will.

	$ /usr/bin/python ./bin/salt --version
	[ ... ]
	ValueError: Expected version spec in [ ... ]
	$ ./bin/python ./bin/salt --version
	salt 2015.8.0-154-g4a69db2 (Beryllium)

If we look at the shebang line of a script file in our virtualenv's `bin` directory, we can see that it specifies the absolute path to the python bin file in our virtualenv:

	$ head -1 bin/salt
	#!/home/andreas/code/python/salt/bin/python2

This means that this particular script will be able to run from anywhere. This also means we can copy or symlink it to any directory in `$PATH`, and we will be able to run it as if it was globally installed.

Personally, I have `~/.local/bin` added to my `$PATH`, but you could also use `~/bin` or `/usr/local/bin`.

	$ ln -s ~/code/python/salt/bin/salt ~/.local/bin/
	$ which salt
	/home/andreas/.local/bin/salt
	$ salt --version
	salt 2015.8.0-154-g4a69db2 (Beryllium)

I'd also like to mention [pipx](https://github.com/pipxproject/pipx) and [psm](https://github.com/anlutro/psm), both of which aim to make this process easier for end-users.
