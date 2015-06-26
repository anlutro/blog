# Russell
pubdate: 2014-03-17 12:00:00

Over the weekend I had a fun little project - writing a tiny static HTML blog generator.

Feeling sick of CMSes and the one I was using in particular not support Postgres, I decided I wanted to switch to a static file system - no backend to care about.

I looked at existing solutions but none of them really spoke to me. Most of the popular ones are written in Ruby, and I will not install a bloated gem (let alone Ruby itself) just to create some html files. I looked at python solutions like pelican but they looked bloated as well. Why would you need more than ~10 files of source code for a static site generator?

So I wrote my own. Named completely at random by something funny that happened the night I had the idea, **Russell** is a static blog HTML generator written in Python 3. It is roughly 200 lines of code, requires a few packages (jinja2, markdown, slugify and docopt) and can be installed from PIP:

	pip install russell

The command `russell` is now available on your command line. `russell -h` will show the help screen.

My own blog is of course now generated using Russell, and I am very happy with it. Head over to the [Github page](https://github.com/anlutro/russell) for more information. I would love to hear your feedback if you decide to try it out!