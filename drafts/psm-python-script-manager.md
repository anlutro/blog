# PSM - Python Script Manager
pubdate: 2019-11-22 20:27 CET

It's fairly common for generally useful CLI tools to be written in Python. Some examples off the top of my head are [ranger](https://github.com/ranger/ranger), [streamlink](https://github.com/streamlink/streamlink), [youtube-dl](https://ytdl-org.github.io/youtube-dl/index.html) and [glances](https://nicolargo.github.io/glances/).

Some of these are available as part of your operating system's package management, but may not be up to date. You can install them using pip, but installing things with pip is a beginner's trap.

If you install using `sudo pip`, you might overwrite packages on the system and break tools that are required for the operating system to work. This is avoidable by using `pip install --user`, which installs packages into `$HOME/.local` instead of globally, but does mean you have to modify your `$PATH` to include `$HOME/.local/bin`.

However, if you try to install two CLI tools which require two different versions of a dependency, you're likely to break one of them. The solution to this is [virtual environments](https://docs.python-guide.org/dev/virtualenvs/), which are fairly straight forward to use when working on a specific project, but not so much for installing things like CLI programs.

There are tools like [pipsi](https://github.com/mitsuhiko/pipsi) and [pipx](https://github.com/pipxproject/pipx) which attempt to solve this: simply run `pipx install ...` and your thing will be installed. There's a chicken-and-egg problem, though: How do you install `pipx`? It's a python CLI tool after all. You end up having to make an exception for this specific tool and use `pip install --user`.

All of this annoyed me, and encouraged me to write [psm](https://github.com/anlutro/psm). It's a stand-alone shell script, so it can just be downloaded and put in a directory in your `$PATH`.
