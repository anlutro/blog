#!/usr/bin/env python3

import os
import os.path
import logging
import sass

import russell.engine
import russell.cli

ROOT_DIR = os.path.dirname(__file__)


def validate_sass_file(sass_file):
    uses_tabs = None
    with open(sass_file) as file:
        line_no = 0
        for line in file:
            line_no += 1
            if uses_tabs is None:
                if line.startswith("  "):
                    uses_tabs = False
                elif line.startswith("\t"):
                    uses_tabs = True
            elif uses_tabs is True and "  " in line:
                print(
                    "%s uses tabs but spaces found on line #%d" % (sass_file, line_no)
                )
            elif uses_tabs is False and "\t" in line:
                print("%s uses spaces but tab found on line #%d" % (sass_file, line_no))


def generate_css():
    sass_dir = os.path.join(ROOT_DIR, "sass")
    sass_files = [f.path for f in os.scandir(sass_dir) if f.path.endswith(".sass")]
    for sass_file in sass_files:
        validate_sass_file(sass_file)
    sass_main = os.path.join(sass_dir, "main.sass")
    return sass.compile(filename=sass_main)


args = russell.cli.get_args()

logging.basicConfig(
    level=logging.DEBUG if args.verbose else logging.INFO,
    format="%(asctime)s %(levelname)8s [%(name)s] %(message)s",
)

blog = russell.engine.BlogEngine(
    ROOT_DIR,
    root_url=args.root_url or "http://localhost:8000",
    site_title="lutro.me",
    site_desc=(
        "Andreas Lutro's personal website/blog. "
        "Mostly programming and Linux sysadmin stuff."
    ),
    cache_busting_strategy="qs",
)
blog.add_pages()
blog.add_posts()


def generate():
    blog.copy_assets()
    blog.write_file("assets/style.css", generate_css())
    blog.add_asset_hashes()

    blog.generate_index(num_posts=4)
    blog.generate_archive()
    blog.generate_pages()
    blog.generate_posts()
    blog.generate_tags()

    # blog.generate_page('links', template='links.html.jinja')

    blog.generate_sitemap(https=True)

    blog.generate_rss(https=True, only_excerpt=False)
    blog.write_file("robots.txt", "\n".join([
        "User-agent: *"
        "Allow: /",
        "",
        "Sitemap: https://www.lutro.me/sitemap.xml"
    ]))


if __name__ == '__main__':
    generate()
