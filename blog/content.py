from datetime import datetime
import logging
import os.path

import markdown
import slugify

LOG = logging.getLogger(__name__)


def _generate_excerpt(body):
	excerpt_parts = []
	# iterate through lines until we find an empty line/two newlines in a row
	for line in body.splitlines():
		if line == '':
			break
		excerpt_parts.append(line)
	return ' '.join(excerpt_parts)


def _parse_pubdate(pubdate):
	formats = ('%Y-%m-%d %H:%M:%S %z', '%Y-%m-%d %H:%M:%S', '%Y-%m-%d')
	for dateformat in formats:
		try:
			return datetime.strptime(pubdate, dateformat)
		except ValueError:
			pass
	raise ValueError('Could not datetime.strptime {}'.format(repr(pubdate)))


def _str_to_bool(string):
	norm_string = str(string).strip().lower()
	if norm_string in ('yes', 'true'):
		return True
	elif norm_string in ('no', 'false', ''):
		return False
	raise ValueError('Invalid boolean string: {}'.format(repr(string)))


class Content:
	cm = None

	@property
	def root_url(self):
		if self.cm:
			return self.cm.root_url
		return '//localhost'


class Entry(Content):
	def __init__(self, title, body, slug=None, subtitle=None):
		self.title = title
		self.body = body
		self.slug = slug or slugify.slugify(title)
		self.subtitle = subtitle

	@property
	def url(self):
		return self.root_url + '/' + self.slug

	@classmethod
	def from_string(cls, contents, kwargs=None):
		if kwargs is None:
			kwargs = {}

		lines = contents.splitlines()
		title = None

		line = lines.pop(0)
		while line != '':
			if not title and line.startswith('#'):
				title = line[1:].strip()
			elif line.startswith('title:'):
				title = line[6:].strip()
			elif line.startswith('subtitle:'):
				kwargs['subtitle'] = line[9:].strip()
			elif line.startswith('comments:'):
				try:
					kwargs['allow_comments'] = _str_to_bool(line[9:])
				except ValueError:
					LOG.warning('invalid boolean value for comments', exc_info=True)

			cls.process_meta(line, kwargs)

			line = lines.pop(0)

		# the only lines left should be the actual contents
		body = '\n'.join(lines).strip()
		if issubclass(cls, Post):
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
		if issubclass(cls, Post) and not kwargs.get('pubdate'):
			timestamp = min(os.path.getctime(path), os.path.getmtime(path))
			kwargs['pubdate'] = datetime.fromtimestamp(timestamp)

		with open(path, 'r') as file:
			entry = cls.from_string(file.read(), kwargs)

		return entry

	def __lt__(self, other):
		return self.title < other.title


class Page(Entry):
	def __init__(self, title, body, slug=None, subtitle=None, allow_comments=False):
		super().__init__(title, body, slug=slug, subtitle=subtitle)
		self.allow_comments = allow_comments


class Post(Entry):
	def __init__(self, title, body, slug=None, subtitle=None, pubdate=None,
			excerpt=None, tags=None, public=True, allow_comments=True):
		super().__init__(title, body, slug=slug, subtitle=subtitle)
		self.excerpt = excerpt or _generate_excerpt(body)
		self.pubdate = pubdate
		self.tags = tags or []
		self.public = public
		self.allow_comments = allow_comments

	@classmethod
	def make_tag(cls, tag_name):
		if cls.cm:
			return cls.cm.make_tag(tag_name)
		return Tag(tag_name.strip())

	@classmethod
	def process_meta(cls, line, kwargs):
		super().process_meta(line, kwargs)

		if line.startswith('pubdate:'):
			pubdate_str = line[8:].strip()
			try:
				kwargs['pubdate'] = _parse_pubdate(pubdate_str)
			except ValueError:
				LOG.warning('invalid pubdate given', exc_info=True)
			if 'pubdate' in kwargs and not kwargs['pubdate'].tzinfo:
				LOG.warning('found pubdate without timezone: "%s"', pubdate_str)

		elif line.startswith('tags:'):
			line_tags = line[5:].strip().split(',')
			kwargs['tags'] = [cls.make_tag(tag) for tag in line_tags]

		elif line.startswith('public:'):
			try:
				kwargs['public'] = _str_to_bool(line[7:])
			except ValueError:
				LOG.warning('invalid boolean value for public', exc_info=True)

		elif line.startswith('private:'):
			try:
				kwargs['private'] = not _str_to_bool(line[7:])
			except ValueError:
				LOG.warning('invalid boolean value for private', exc_info=True)

	@property
	def url(self):
		return self.root_url + '/posts/' + self.slug

	@property
	def tag_links(self):
		return ['<a href="' + tag.url + '">' + tag.title + '</a>' for tag in self.tags]

	def __lt__(self, other):
		if self.pubdate == other.pubdate:
			return self.title < other.title
		return self.pubdate > other.pubdate


class Tag(Content):
	def __init__(self, title, slug=None):
		self.title = title
		self.slug = slug or slugify.slugify(title)

	@property
	def url(self):
		return self.root_url + '/tags/' + self.slug

	def __lt__(self, other):
		return self.title < other.title


class ContentManager:
	def __init__(self, root_url):
		self.Page = type('CM_Page', (Page,), {'cm': self})
		self.Post = type('CM_Post', (Post,), {'cm': self})
		self.Tag = type('CM_Tag', (Tag,), {'cm': self})
		self.root_url = root_url
		self.pages = []
		self.posts = []
		self.tags = []
		self.tags_dict = {}

	def make_tag(self, tag_name):
		tag_name = tag_name.strip()
		if tag_name not in self.tags_dict:
			self.tags_dict[tag_name] = self.Tag(tag_name)
		return self.tags_dict[tag_name]

	def add_pages(self, pages, resort=True):
		self.pages.extend(pages)
		if resort:
			self.pages.sort()

	def add_posts(self, posts, resort=True):
		self.posts.extend(posts)
		for post in posts:
			for tag in post.tags:
				if tag not in self.tags:
					self.tags.append(tag)

		if resort:
			self.tags.sort()
			self.posts.sort()
