#!/usr/bin/env python3

import argparse
import os
import os.path
from blog.engine import BlogEngine

ROOT_DIR = os.path.dirname(__file__)

def _extract_domain(value):
	value = value.split('//', 1)[1]
	value = value.split('/', 1)[0]
	return value.replace('www.', '')

parser = argparse.ArgumentParser()
parser.add_argument('--root-url', default='//www.lutro.me')
args = parser.parse_args()

blog = BlogEngine(ROOT_DIR, site_title='lutro.me', root_url=args.root_url)
blog.jinja.filters['extract_domain'] = _extract_domain
blog.add_pages()
blog.add_posts()
blog.add_data()

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
