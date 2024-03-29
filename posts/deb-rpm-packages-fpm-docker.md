# Building deb/rpm packages with FPM in Docker
pubdate: 2019-12-17 18:23 +0100
tags: Packaging, Deployment, Docker

Whether you're building on-premise software or just want to use packages as your atomic deployment mechanism of choice in a traditional bare-metal/VM infrastructure, deb/rpm packages are a nice thing to provide.

Unfortunately, building them is super tedious. Try googling for official documentation on how to build Debian packages and you'll find at least 5 official wiki pages all with slight variations. Redhat packages are a bit better but still rather tedious. Luckily, there's a program which has our back: [FPM - Effing Package Management](https://fpm.readthedocs.io).

Looking into how to run this on an engineer's laptop as easily as in a CI/CD pipeline, annoyances keep piling up.

1. Running FPM with the correct arguments is annoying. Let's put the invocations in a shell script or Makefile.
1. We don't want to have to install FPM on our main system - it requires ruby, gems and more. Let's run it in a Docker container. Luckily, there exists a Docker image which contains FPM and its dependencies, as well as optional dependencies for extra features: [eclecticiq/package](https://hub.docker.com/r/eclecticiq/package)
1. The application runtime (binaries, libraries...) needs to be available in the same container, otherwise FPM doesn't know what to package. Let's use multi-stage Docker builds to build the application and make the resulting files available to the FPM container.
1. Running docker build, docker run, then copying files out of the docker container is annoying. Let's put the invocations in the Makefile or another shell script.

With all of the above fixed, you end up with a single Makefile target or shell script which would build the project's deb/rpm packages for me, either on my laptop or in the CI/CD system of my choice.

A complete example of how to build, run, and package an application using this system is available on Github: [fpm-docker-example](https://github.com/anlutro/fpm-docker-example)

It has a few branches which are worth checking out: The default branch is a simple Golang example, but there's also a branch for Python applications, and one showing how the process can be simplified using [Earthly](https://earthly.dev).
