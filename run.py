#!/usr/bin/env python3

import argparse
import os.path
import logging
import sass
from russell.engine import BlogEngine

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

blog.generate_index(num_posts=3)
blog.generate_archive()
blog.generate_pages()
blog.generate_posts()
blog.generate_tags()

blog.generate_page('links', template='links.html.jinja')

blog.generate_sitemap(https=True)

blog.generate_rss('rss.xml')
blog.write_file('robots.txt', 'User-agent: *\nDisallow:\n')
