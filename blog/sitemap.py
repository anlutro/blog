from xml.etree import ElementTree as etree

def text_element(tag, text):
	el = etree.Element(tag)
	el.text = text
	return el

def generate_sitemap(blog):
	tree = etree.Element('urlset', xmlns='http://www.sitemaps.org/schemas/sitemap/0.9')
	tree.append(get_index_element(blog.root_url))
	for page in blog.pages:
		tree.append(get_page_element(page))
	for tag in blog.tags:
		tree.append(get_tag_element(tag))
	for post in blog.get_posts():
		tree.append(get_post_element(post))
	return etree.tostring(tree, 'utf-8')

def get_post_element(post):
	el = etree.Element('url')
	el.append(text_element('loc', post.url))
	el.append(text_element('lastmod', post.pubdate.strftime('%Y-%m-%d')))
	el.append(text_element('changefreq', 'monthly'))
	return el

def get_page_element(page):
	el = etree.Element('url')
	el.append(text_element('loc', page.url))
	el.append(text_element('changefreq', 'monthly'))
	return el

def get_tag_element(tag):
	el = etree.Element('url')
	el.append(text_element('loc', tag.url))
	el.append(text_element('changefreq', 'weekly'))
	return el

def get_index_element(url):
	el = etree.Element('url')
	el.append(text_element('loc', url))
	el.append(text_element('changefreq', 'daily'))
	return el
