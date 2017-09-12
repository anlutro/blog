#!/usr/bin/env python

import os
import os.path
from http.server import HTTPServer, SimpleHTTPRequestHandler


class RequestHandler(SimpleHTTPRequestHandler):
	def translate_path(self, path):
		path = super().translate_path(path)
		try_paths = (path, path + '.html', path + '/index.html')
		for try_path in try_paths:
			if os.path.exists(try_path):
				return try_path
		return path


def run_server(root_dir=None):
	if root_dir:
		os.chdir(root_dir)

	server_address = ('127.0.0.1', 8000)

	httpd = HTTPServer(server_address, RequestHandler)
	sa = httpd.socket.getsockname()
	print('Serving HTTP on http://%s:%s/ ...' % sa)
	try:
		httpd.serve_forever()
	except KeyboardInterrupt:
		pass
	finally:
		httpd.server_close()

run_server(os.path.join(os.path.dirname(__file__), 'dist'))
