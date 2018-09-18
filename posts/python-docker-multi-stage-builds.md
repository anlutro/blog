# Multi-stage Docker builds for Python projects
pubdate: 2018-08-06 21:34 CEST
tags: Python, Docker

Multi-stage builds can help reduce your Docker image sizes in production. This has many benefits: Development dependencies may potentially expose extra security holes in your system (I've yet to see this happen, but why not be cautious if it's easy to be so?), but mostly by reducing image size you make it faster for others to `docker pull` it.

The concept of multi-stage builds is simple: Install development dependencies, build all the stuff you need, then copy over just the stuff you need to run in production in a brand new image without installing development dependencies not needed to run the application.

Here's an example Dockerfile using the official Python Docker images, which are based on Debian - but you can easily apply the same principle when building from Debian, Ubuntu, CentOS, or Alpine images: Have one stage where build/development dependencies are installed and the application is built, and another where runtime dependencies are installed and the application is ran.

	FROM python:3.7-stretch AS build
	RUN python3 -m venv /venv

	# example of a development library package that needs to be installed
	RUN apt-get -qy update && apt-get -qy install libldap2-dev && \
	    rm -rf /var/cache/apt/* /var/lib/apt/lists/*

	# install requirements separately to prevent pip from downloading and
	# installing pypi dependencies every time a file in your project changes
	ADD ./requirements /project/requirements
	ARG REQS=base
	RUN /venv/bin/pip install -r /project/requirements/$REQS.txt

	# install the project, basically copying its code, into the virtualenv.
	# this assumes the project has a functional setup.py
	ADD . /project
	RUN /venv/bin/pip install /project

	# this won't have any effect on our production image, is only meant for
	# if we want to run commands like pytest in the build image
	WORKDIR /project


	# the second, production stage can be much more lightweight:
	FROM python:3.7-slim-stretch AS production
	COPY --from=build /venv /venv

	# install runtime libraries (different from development libraries!)
	RUN apt-get -qy update && apt-get -qy install libldap-2.4-2 && \
	    rm -rf /var/cache/apt/* /var/lib/apt/lists/*

	# remember to run python from the virtualenv
	CMD ["/venv/bin/python3", "-m", "myproject"]

Copying the virtual environment is by far the easiest approach to this problem. Python purists will say that virtual environments shouldn't be copied, but when the underlying system is the same and the path is the same, it makes literally no difference (plus virtual environments are a dirty hack to begin with, one more dirty hack doesn't make a difference).

There are a few alternate approaches, the most relevant of which is to build a wheel cache of your dependencies and mount that in as a volume. The problem with this is that Docker doesn't let you mount volumes in the build stage, so you have to make complex shell scripts and multiple Dockerfiles to make it work, and the only major advantage is that you don't always have to re-compile wheels (which should be on pypi anyway, and my dependencies don't change that often).

Another thing of note: In our example, we install both project dependencies *and* the project itself into the virtualenv. This means we don't even need the project root directory in the production image, which is also nice (no risk of leaking example configuration files, git history etc.).

To build the image and run our project, assuming it's a webserver listening on port 5000, these commands should let you visit http://localhost:5000 in your browser:

	$ docker build --tag=myproject .
	$ docker run --rm -it -p5000:5000 myproject

### Running tests

What if we want to build an image for running tests, which require some extra development dependencies? That's where the purpose of our `ARG REQS` comes in. By setting this build argument when running `docker build`, we can control which requirements file is read. Combine that with the `--target` argument to `docker run` and this is how you build a development/testing image:

	$ docker build --target=build --build-arg REQS=dev --tag=myproject-dev .

And let's say you want to run some commands using that image:

	$ docker run --rm -it myproject-dev /venv/bin/pytest
	$ docker run --rm -it myproject-dev bash

### Development in Docker

Note that you'll have to re-build the image any time code changes. I don't care too much about this since I do all my development locally anyway, and only use Docker for production and continuous integration, but if it's important to you, you'll have to:

1. Change `pip install /project` to `pip install -e /project`
2. Copy the entire `/project` directory into the production image as well
3. Mount the project's root directory as `/project` with `docker run --volume=$PWD:/project`

### Example project

If you want a functional example to play around with, I've got a git repository on Github with a sample Python project which has a docker-multistage branch: [python-project-examples](https://github.com/anlutro/python-project-examples/tree/docker-multistage)
