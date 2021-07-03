# Better ways of managing pip dependencies
pubdate: 2017-11-06 18:57 +0100
tags: Python, pip

Of all the languages I've worked with, Python is one of the most annoying to work with when it comes to managing dependencies - only Go annoys me more. The industry standard is to keep a strict list of your dependencies (and their dependencies) in a `requirements.txt` file. Handily, this can be auto-generated with `pip freeze > requirements.txt`.

What's the problem with requirement files? It's not really a problem as long as you only have one requirements file, but if you want to start splitting up dev vs test/staging vs production dependencies, you'll immediately run into problems.

The most common solution is to have a `requirements` directory with `base.txt`, `dev.txt`, `prod.txt` and so on for whatever environments/contexts you need. The problem with this approach starts showing up when you want to add or upgrade a package and its dependencies - because you no longer have a single requirements file, you can't simply `pip freeze > requirements.txt`, so you end up carefully updating the file(s) by hand.

There are some existing third-party tools out there written to help with this problem. Two of them create entirely new formats of storing information on dependencies:

- [pipenv](https://github.com/kennethreitz/pipenv)/[pipfile](https://github.com/pypa/pipfile) uses a completely new file format for storing dependencies, inspired by other language's more modern dependency managers. In the future this may be part of pip core, but it is not currently. Until then I'm staying far away from the project, as trying to implement it in a real-world project revealed all sorts of bugs. The codebase itself looks super sketchy, as it's downloaded upstream libraries like pip, but then applied patches on top of them.
- [poetry](https://poetry.eustace.io/) is a far more promising project. Its goals are similar to that of pipenv but it just seems to have been developed in a more sane way. It uses the PEP518 `pyproject.toml` file to store information about which dependencies should be installed.

Some other tools aim to stick closer to the existing workflow of requirement files:

- [pipwrap](https://github.com/jessamynsmith/pipwrap) scans your virtualenv for packages, compares them to what's in your requirements files, and interactively asks you where it should place packages that are in your environment, but not in any requirements file.
- pip-compile (part of [pip-tools](https://github.com/jazzband/pip-tools)) lets you write more minimal `requirements.in` files, and auto-generates strict version `requirements.txt` files based on them. As a bonus you get to see where your nested dependencies are coming from.

There is also an existing solution that works without introducing third-party tools. Since version 7.1, there is a `--constraint` flag to the `pip install` command which can be used to solve this problem.

A constraint file is an additional requirements file which won't be used to determine **which** packages to install, but will be used to lock down versions for any packages that **do** get installed. This means that you can put your base requirements (that is, you don't need to include dependencies of dependencies) in your requirements file, then store version locks for **all** environments in a separate constraint file.

First of all, we want to make sure we never forget to add `--constraint constraint.txt` by adding it to the top of our `requirements/base.txt` file (and any other requirements file that does not include `-r base.txt`). Next, generate the constraint file with `pip freeze > requirements/constraint.txt`. You can now modify all your requirements files, removing or loosening version constraint, and removing nested dependencies.

With that out of the way, let's look at some example workflows. Upgrade an existing package:

```bash
pip install 'django >= 2'
# no need to edit requirements/base.txt, "django" is already there
pip freeze > requirements/constraint.txt
```

Install a new package in dev:

```bash
echo 'pytest-cov' >> requirements/dev.txt
pip install -r requirements/dev.txt
pip freeze > requirements/constraint.txt
```

Install requirements in a fresh production or development environment works just like before:

```bash
pip install -r requirements/base.txt
pip install -r requirements/dev.txt
```

This isn't perfect. If you don't install *every* requirement file in development, your constraint file will be missing those files' requirements. A code review would catch accidentally removing a constraint, but how do you detect a package that is entirely missing from the constraint file? `pip install` doesn't even have a dry-run mode. Still, constraint files (or any of the third-party tools, really) are nice ways of improving and simplifying dependency managment with `pip`.

There's also a shell command you can use as a commit hook or part of your test/CI suite to check that you're not missing anything in your constraint.txt:

```bash
! pip freeze | grep -vxiF -f requirements/constraint.txt -
```

This will output all pip packages that are installed but not present in your constraint file. We use the `!` to make sure that the command gives a non-zero exit code if there are any matches.
