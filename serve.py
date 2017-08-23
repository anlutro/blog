#!/usr/bin/env python

import os
import os.path
from http.server import test, SimpleHTTPRequestHandler

class RequestHandler(SimpleHTTPRequestHandler):
	def translate_path(self, path):
		path = super().translate_path(path)
		try_paths = (path, path + '.html', path + '/index.html')
		for try_path in try_paths:
			if os.path.exists(try_path):
				return try_path
		return path

os.chdir(os.path.join(os.path.dirname(__file__), 'dist'))
test(HandlerClass=RequestHandler)
