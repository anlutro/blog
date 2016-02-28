# Cache busting URLs with Flask and Nginx
pubdate: 2016-01-16 08:30:48
tags: Flask, Nginx, Python

In this post, I'll show you how to effectively override Flask's `url_for` function in order to add a timestamp to static asset URLs, as well as setting up Nginx to serve cache busted URLs.

	import flask
	app = flask.Flask()

	def cache_busting_url_for(static_dir, old_url_for, bust_extensions=True):
		def transform_filename(orig_filename):
			file_path = os.path.join(static_dir, orig_filename)
			if os.path.isfile(file_path):
				timestamp = int(os.stat(file_path).st_mtime)
				directory, filename = os.path.split(orig_filename)
				filename, extension = filename.split('.', 1)
				if bust_extensions is True or extension in bust_extensions or \
						extension.split('.')[-1] in bust_extensions:
					filename = '{}.{}.{}'.format(filename, timestamp, extension)
					return os.path.join(directory, filename)
			return orig_filename

		url_cache = {}

		def url_for_wrapper(endpoint, **values):
			if endpoint == 'static':
				filename = values.get('filename')
				if filename:
					if filename not in url_cache:
						url_cache[filename] = transform_filename(filename)
					values['filename'] = url_cache[filename]
			return old_url_for(endpoint, **values)

		return url_for_wrapper

	flask.url_for = cache_busting_url_for(app.static_folder, flask.url_for)

`cache_busting_url_for` is a function that returns another function. In this example, we've omitted the `bust_extensions` argument, which means every single static URL will get timestamped. In reality, you'll probably want to pass a list or tuple of extensions that you want to cache bust.

Next, we need to set up our Nginx configuration to rewrite cache busted URLs to real URLs ("static/style.1452929749.css" to "static/style.css").

	location /static {
		location ~* ^(.+)\.\d+\.((min\.)?js|css(\.map)?)$ {
			try_files $uri $1.$2;
		}

		# more nginx configuration for static files here
	}

In this regex, you need to make sure that whatever file extensions you want to cache bust are matched correctly. In my case, I want both minified and not minified JS/CSS files to match, as well as their corresponding source maps.

`\.\d+\.` is the regex that matches the timestamp that we added to our asset URLs. Notice how it's not captured by any regex groups (denoted by parenthesis), so when we rewrite the url to `$1.$2`, the timestamp has been removed.
