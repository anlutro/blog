from datetime import datetime
import hashlib
import logging
import os
import os.path

import jinja2
import PyRSS2Gen
import yaml

import blog.content

LOG = logging.getLogger(__name__)


def _listfiles(root_dir):
	results = set()

	for root, _, files in os.walk(root_dir):
		for file in files:
			results.add(os.path.join(root, file))

	return results


def _parse_data_file(path):
	if path.endswith('.yaml') or path.endswith('.yml'):
		return yaml.load(open(path, 'r'))
	raise ValueError('Do not know how to parse data file: ' + path)


def _rss_item(post):
	return PyRSS2Gen.RSSItem(
		title=post.title,
		description=post.excerpt,
		link=post.url,
		pubDate=post.pubdate,
	)


class BlogEngine:
	def __init__(self, root_path, root_url, site_title, site_desc=None):
		self.root_path = root_path
		self.root_url = root_url
		self.site_title = site_title
		self.site_desc = site_desc

		self.cm = blog.content.ContentManager(root_url)
		self.pages = self.cm.pages
		self.posts = self.cm.posts
		self.tags = self.cm.tags

		self.data = {}

		self.jinja = jinja2.Environment(
			loader=jinja2.FileSystemLoader(os.path.join(root_path, 'templates')),
		)
		self.jinja.globals.update({
			'a': self.get_link,
			'asset_url': self.get_asset_url,
			'now': datetime.now(),
			'root_url': self.root_url,
			'site_description': self.site_desc,
			'site_title': self.site_title,
			'tags': self.tags,
		})

	def get_asset_url(self, path):
		url = self.root_url + '/assets/' + path
		if 'asset_hash' in self.data and path in self.data['asset_hash']:
			url += '?' + self.data['asset_hash'][path]
		return url

	def get_link(self, title, url, blank=None):
		attrs = 'href="{}"'.format(url)
		if blank:
			attrs += ' target="_blank" rel="noopener noreferrer"'
		return '<a {}>{}</a>'.format(attrs, title)

	def add_pages(self, path='pages'):
		path = os.path.join(self.root_path, path)
		self.cm.add_pages([
			self.cm.Page.from_file(file)
			for file in _listfiles(path)
		])

	def add_posts(self, path='posts'):
		path = os.path.join(self.root_path, path)
		self.cm.add_posts([
			self.cm.Post.from_file(file)
			for file in _listfiles(path)
		])

	def add_data_files(self, path='data'):
		path = os.path.join(self.root_path, path)
		for file in os.listdir(path):
			file_path = os.path.join(path, file)
			if not os.path.isfile(file_path):
				continue
			key = file.split('.')[0]
			self.data[key] = _parse_data_file(file_path)
			self.jinja.globals[key] = self.data[key]

	def add_asset_hashes(self, path='dist/assets'):
		if 'asset_hash' not in self.data:
			self.data['asset_hash'] = {}
		if 'asset_hash' not in self.jinja.globals:
			self.jinja.globals['asset_hash'] = {}
		for fullpath in _listfiles(os.path.join(self.root_path, path)):
			relpath = fullpath.replace(self.root_path + '/' + path + '/', '')
			md5sum = hashlib.md5(open(fullpath, 'rb').read()).hexdigest()
			LOG.debug('MD5 of %s (%s): %s', fullpath, relpath, md5sum)
			self.data['asset_hash'][relpath] = md5sum
			self.jinja.globals['asset_hash'][relpath] = md5sum

	def get_posts(self, num=None, tag=None, private=False):
		posts = self.posts.copy()
		if not private:
			posts = [post for post in posts if post.public]
		if tag:
			posts = [post for post in posts if tag in post.tags]
		if num:
			return posts[:num]
		return posts

	def _get_dist_path(self, path):
		if isinstance(path, str):
			path = [path]
		return os.path.join(self.root_path, 'dist', *path)

	def _get_template(self, template):
		if isinstance(template, str):
			template = self.jinja.get_template(template)
		return template

	def generate_page(self, path, template, **kwargs):
		path = self._get_dist_path(path)
		if not path.endswith('.html'):
			path = path + '.html'
		if not os.path.isdir(os.path.dirname(path)):
			os.makedirs(os.path.dirname(path))
		template = self._get_template(template)
		with open(path, 'w+') as file:
			file.write(template.render(**kwargs))

	def generate_rss(self, path, posts):
		rss = PyRSS2Gen.RSS2(
			title=self.site_title,
			description='',
			link=self.root_url,
			lastBuildDate=datetime.now(),
			items=[_rss_item(post) for post in posts],
		)

		path = self._get_dist_path(path)
		with open(path, 'w+') as file:
			rss.write_xml(file)

	def write_file(self, path, contents):
		path = self._get_dist_path(path)
		if isinstance(contents, bytes):
			mode = 'wb+'
		else:
			mode = 'w'
		with open(path, mode) as file:
			file.write(contents)
