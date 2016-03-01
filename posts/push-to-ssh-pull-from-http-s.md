# Git(hub) - Push via SSH, pull via HTTP(S)
pubdate: 2015-06-26 12:00:00 +0100
tags: Git

I work with public Github repositories a lot, and get super annoyed because I want to push with my SSH key (because I'd rather put in my key's password than my Github username/password), but I want to pull with HTTPS (because then I don't have to put in a username or password). Normally, the way you do this is:

	git clone https://github.com/foo/bar.git
	cd bar
	git set-url origin git@github.com/foo/bar.git --push

However, I found a really cool way of doing this in all your repositories, without having to do anything each time you clone a repository. Add the following to your `~/.gitconfig`:

	[url "git@github.com:"]
	pushInsteadOf = https://github.com/

This will replace "https://github.com" with "git@github.com" in the remote URL, but only when pushing.
