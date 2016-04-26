import blog.content


def test_basic_parsing():
	md = '# Hello world!\n\nThis is a test post.'
	post = blog.content.Post.from_string(md)
	assert 'Hello world!' == post.title
	assert '<p>This is a test post.</p>' == post.body


def test_pubdate_parsing():
	md = '# Hello world!\npubdate:2015-01-01 01:23:45\n\nThis is a test post.'
	post = blog.content.Post.from_string(md)
	assert post.title == 'Hello world!'
	assert post.pubdate.isoformat() == '2015-01-01T01:23:45'
	assert post.body == '<p>This is a test post.</p>'


def test_tag_parsing():
	md = '# Hello world!\ntags:Foo Bar, Bar Baz\n\nThis is a test post.'
	post = blog.content.Post.from_string(md)
	assert post.title == 'Hello world!'
	assert [tag.title for tag in post.tags] == ['Foo Bar', 'Bar Baz']
	assert post.body == '<p>This is a test post.</p>'


def test_generate_excerpt():
	md = ('# Hello world!\n\n'
		'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec\n'
		'maximus diam ut ligula blandit semper. Proin id nulla libero.\n\n'
		'Quisque blandit ut enim in ultricies. Sed sollicitudin aliquam\n'
		'consectetur. In pharetra, justo a ultrices porttitor, quam risus\n'
		'semper dolor, interdum tempus est libero ac tellus.')
	post = blog.content.Post.from_string(md)
	expected = ('<p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. '
		'Donec maximus diam ut ligula blandit semper. Proin id nulla libero.</p>')
	assert post.excerpt == expected


def test_content_manager_root_url():
	cm = blog.content.ContentManager(root_url='//example.com')
	md = '# Hello world!\n\nThis is a test post.'
	post = cm.Post.from_string(md)
	assert post.url == '//example.com/posts/hello-world'


def test_content_manager_tags():
	cm = blog.content.ContentManager(root_url='//example.com')
	md = '# Hello world!\ntags:Foo Bar, Bar Baz\n\nThis is a test post.'
	post1 = cm.Post.from_string(md)
	post2 = cm.Post.from_string(md)
	assert post1.tags[0] is post2.tags[0]
	assert post1.tags[1] is post2.tags[1]
