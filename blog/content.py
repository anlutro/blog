import datetime
import logging
import os.path

import markdown
import slugify

LOG = logging.getLogger(__name__)
ROOT_URL = '//localhost'
_TAGS = {}


def _generate_excerpt(body):
	excerpt_parts = []
	for line in body.splitlines():
		if line == '':
			break
		excerpt_parts.append(line)
	return ' '.join(excerpt_parts)


def _parse_pubdate(pubdate):
	formats = ('%Y-%m-%d %H:%M:%S %z', '%Y-%m-%d %H:%M:%S', '%Y-%m-%d')
	for dateformat in formats:
		try:
			return datetime.datetime.strptime(pubdate, dateformat)
		except ValueError:
			pass
	return None


def make_tag(tag_name):
	tag_name = tag_name.strip()
	if tag_name not in _TAGS:
		_TAGS[tag_name] = Tag(tag_name)
	return _TAGS[tag_name]


class Entry():
	def __init__(self, title, body, slug=None):
		self.title = title
		self.body = body
		self.slug = slug or slugify.slugify(title)

	@property
	def url(self):
		return ROOT_URL + '/' + self.slug

	@classmethod
	def from_file_contents(cls, contents, kwargs=None):
		if kwargs is None:
			kwargs = {}

		lines = contents.splitlines()
		title = None

		line = lines.pop(0)
		while line != '':
			if not title and line.startswith('#'):
				title = line.replace('#', '').strip()
			elif line.startswith('title:'):
				title = line[6:].strip()

			cls.process_meta(line, kwargs)

			line = lines.pop(0)

		# the only lines left should be the actual contents
		body = '\n'.join(lines).strip()
		if cls is Post:
			kwargs['excerpt'] = markdown.markdown(
				_generate_excerpt(body)
			)
		body = markdown.markdown(body)

		return cls(title=title, body=body, **kwargs)

	@classmethod
	def process_meta(cls, line, kwargs):
		if line.startswith('slug:'):
			kwargs['slug'] = line[5:].strip()

	@classmethod
	def from_file(cls, path, kwargs=None):
		if kwargs is None:
			kwargs = {}

		LOG.debug('creating %s from "%s"', cls, path)

		# the filename will be the default slug - can be overridden later
		kwargs['slug'] = os.path.splitext(os.path.basename(path))[0]

		# if a pubdate wasn't found, use the file's last modified time
		if cls is Post and not kwargs.get('pubdate'):
			timestamp = min(os.path.getctime(path), os.path.getmtime(path))
			kwargs['pubdate'] = datetime.datetime.fromtimestamp(timestamp)

		with open(path, 'r') as file:
			entry = cls.from_file_contents(file.read(), kwargs)

		return entry


class Page(Entry):
	pass


class Post(Entry):
	def __init__(self, title, body, slug=None, pubdate=None, excerpt=None,
			tags=None, public=True):
		super().__init__(title, body, slug)
		self.excerpt = excerpt or _generate_excerpt(body)
		self.pubdate = pubdate
		self.tags = tags or []
		self.public = public

	@classmethod
	def process_meta(cls, line, kwargs):
		super().process_meta(line, kwargs)

		if line.startswith('pubdate:'):
			pubdate_str = line[8:].strip()
			pubdate = _parse_pubdate(pubdate_str)
			if pubdate:
				kwargs['pubdate'] = pubdate
			else:
				LOG.warning('found invalid pubdate: "%s"', pubdate_str)
			if not pubdate.tzinfo:
				LOG.warning('found pubdate without timezone: "%s"', pubdate_str)

		elif line.startswith('tags:'):
			kwargs['tags'] = [make_tag(tag) for tag in line[5:].strip().split(',')]

		elif line.startswith('public:'):
			is_public = line[7:].strip().lower()
			if is_public in ('yes', 'true'):
				kwargs['public'] = True
			elif is_public in ('no', 'false'):
				kwargs['public'] = False
			else:
				LOG.warning('found invalid public value: %s', is_public)

	@property
	def url(self):
		return ROOT_URL + '/posts/' + self.slug

	@property
	def tag_links(self):
		return ['<a href="' + tag.url + '">' + tag.title + '</a>' for tag in self.tags]


class Tag:
	def __init__(self, title, slug=None):
		self.title = title
		self.slug = slug or slugify.slugify(title)

	@property
	def url(self):
		return ROOT_URL + '/tags/' + self.slug

	def __lt__(self, other):
		return self.slug < other.slug

