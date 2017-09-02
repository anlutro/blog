# Proper logging in Django
pubdate: 2017-09-02 10:03 +0200
tags: Python, Django

Setting up logging in a sane way in Django has been surprisingly difficult due to some confusing setting names and the annoying way Django's default logging setup looks like. Here I'll go through some simple steps you can take to gain full control of your logging setup, without too many changes to a standard Django setup.

First of all, set `LOGGING_CONFIG = None` to prevent Django from setting up logging for you at all. You want this because in addition to the `LOGGING` dict that you define, Django has some [defaults settings](https://github.com/django/django/blob/18dd9ba4812fb85297a6fab19ea2404cd60b8ad0/django/utils/log.py#L12-L73) it will use, which you may not want.

Because we've set this, we need to call `logging.dictConfig(LOGGING)` ourselves. This can happen at the end of your settings file.

Make sure that `LOGGING['disable_existing_loggers'] = False`. If this is set to true, any loggers defined or invoked before `logging.dictConfig` is called will **silently discard all its messages**. You definitely don't want that.

Finally, I like to define `LOGGING['root']` to have one log instance that controls everything, but sometimes log messages don't get sent to it. I found that setting the `""` (empty string) logger can fix this:

	LOGGING['loggers'][''] = { 'propagate': True }
