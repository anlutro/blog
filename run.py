#!/usr/bin/env python3

import argparse
import os.path
import logging
import sass
from blog.engine import BlogEngine
from blog.sitemap import generate_sitemap

ROOT_DIR = os.path.dirname(__file__)

logging.basicConfig()

def _extract_domain(value):
	value = value.split('//', 1)[1]
	value = value.split('/', 1)[0]
	return value.replace('www.', '')

parser = argparse.ArgumentParser()
parser.add_argument('--root-url', default='//www.lutro.me')
args = parser.parse_args()

blog = BlogEngine(
	ROOT_DIR,
	root_url=args.root_url,
	site_title='lutro.me',
	site_desc=("Andreas Lutro's personal website/blog. "
	           "Mostly programming and Linux sysadmin stuff.")
)
blog.jinja.filters['extract_domain'] = _extract_domain
blog.add_pages()
blog.add_posts()

blog.write_file('assets/style.css', sass.compile(
	filename=os.path.join(ROOT_DIR, 'sass', 'main.sass')
))

blog.add_asset_hashes()

blog.generate_page('index', template='home.html.jinja',
	posts=blog.get_posts(num=3))

blog.generate_page('archive', template='archive.html.jinja',
	posts=blog.get_posts())

for page in blog.pages:
	blog.generate_page(page.slug, template='page.html.jinja',
		page=page)

for post in blog.posts:
	blog.generate_page(['posts', post.slug], template='post.html.jinja',
		post=post)

for tag in blog.tags:
	blog.generate_page(['tags', tag.slug], template='archive.html.jinja',
		posts=blog.get_posts(tag=tag, private=True))

blog.generate_page('links', template='links.html.jinja')

blog.generate_rss('rss.xml', posts=blog.get_posts())

blog.write_file('robots.txt', 'User-agent: *\nDisallow:\n')

if not args.root_url.startswith('file://'):
	blog.write_file('sitemap.xml', generate_sitemap(blog, https=True))
