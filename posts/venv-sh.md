# venv.sh - sensible virtualenv workflow
pubdate: 2020-06-04 22:36 +0200
tags: Python

Virtual environments can be kind of cryptic to people who haven't worked with Python for a while. I'd say that even for people that do work with Python, it can take a long time for it to "click". The short version is, you want one virtual environment for every Python project you work on, which, if you work on a lot of smaller projects, can get annoying.

The standard method of creating and using a virtualenv looks something like this:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip setuptools
```

Now you're ready to install the project itself and its dependencies. Kind of verbose, though you do only have to run `source .venv/bin/activate` in the future - but if you forget whether you've created a virtual environment for a project (directory), it gets more tedious.

Wanting a more ergonomic solution to this, I've worked on some shell functions which I've now put in a Github repository: [`venv.sh`](https://github.com/anlutro/venv.sh).

It allows me to just run the command `venv activate` (I've actually aliased it to `av` so even less typing), and it will activate a virtual environment if one is found in the current working directory, otherwise it will create it for you using the newest version of Python found on your system (only by default, of course).

If you find it annoying to work with virtual environments and other solutions like virtualenvwrapper or direnv don't feel right, check it out.
