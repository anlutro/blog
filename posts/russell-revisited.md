# Russell, revisited
pubdate: 2017-09-12 18:58 CEST
tags: Python

3 years ago I wrote about [/posts/russell](Russell), a static site/blog generator I wrote. Since then, I've had a major rewrite of the project to make it easier to extend and configure.

My sentiments towards other static site generators and CMSes are still the same, though at least by now the most popular ones aren't all written in Ruby.

I realized quickly though that I wanted more control over how my site was to be generated. I didn't want to be limited to what could be expressed in a YAML file - it basically meant that I would have to think ahead of anything that the user of Russell would want to do, and add support for that in the code that reads the YAML config and acts upon it.

The solution to this was simple: Use Python to run and configure Russell instead. When you run `russell setup` to create a new Russell site, the main entrypoint will be `run.py`.

Furthermore, I now recommend that you install Russell into a virtualenv which you can bring in other dependencies to as well. For example, in the source code for the website you're reading now, I bring in `libsass` to compile Sass files into CSS.

	blog.write_file('assets/style.css', sass.compile(
		filename=os.path.join(ROOT_DIR, 'sass', 'main.sass')
	))

If you're looking for a static site generator, especially for a blog or similar, and you like Python, I recommend now more than ever to check out [Russell](https://github.com/anlutro/russell)!
