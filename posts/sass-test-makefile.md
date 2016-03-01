# SASS tests with a simple Makefile
pubdate: 2014-12-14 12:00:00 +0100
tags: Sass, Make

Working with increasingly complex SASS mixins and functions recently, I wanted to set up some sort of test suite to check the CSS output of various files. Rather than bother with some silly NPM package/Ruby gem, I figured I might as well just use some basic shell commands that can be placed in a Makefile (which I already had anyway).

Assume you have your SASS files placed in a directory named `sass`. Create the directory `sass/tests` - this is where we'll place our test files.

We'll create one .sass file for each feature we want to test, as well as a file with the same name, but with the extension .expected.css - which, as you may have guessed, will contain the expected CSS output of the SASS file.

We can leverage the `diff` program to check for differences in output. We'll pipe the SASS compiler's output to it, and make it compare to the .expected.css file, like this:

	css.test:
		for f in sass/tests/*.sass; do \
			sassc $$f | diff - $${f%.sass}.expected.css \
			&& echo OK: $$f; done

`${f%.sass}` is a neat bash trick to remove an extension from a path string. The output on success will look something like this:

	$ make css.test 
	for f in style/tests/*.sass; do \
		sassc $f | diff - ${f%.sass}.expected.css \
		&& echo OK: $f; done
	OK: style/tests/columns.sass

Output on failure will look something like this:

	$ make css.test 
	for f in style/tests/*.sass; do \
		sassc $f | diff - ${f%.sass}.expected.css \
		&& echo OK: $f; done
	4c4
	<   width: 27.33333%;
	---
	>   width: 29.33333%;
	Makefile:130: recipe for target 'css.test' failed
	make: *** [css.test] Error 1
