# Different SSH keys per github organisation
pubdate: 2017-08-23T19:13:44+02:00
tags: Linux, Git

If you're like me, you prefer seting up different SSH keys for personal and professional use. Maybe you even work for multiple organisations at the same time and don't want to risk 1 compromised private key to have a wide-spread effect.

First, we need to set up our SSH config. We'll use a fake hostname for our github organisation. Put this in your `~/.ssh/config`:

```
host example.github.com
	hostname github.com
	identityfile ~/.ssh/id_example_rsa
```

This will make sure that when we do any SSH (and indirectly, git) operations against the domain "example.github.com", the correct SSH key will be used.

We could just remember to replace github.com with example.github.com every time we git clone or add a remote URL, but that's tedious. Instead, we can set up git in a way that does this automatically for us. This is what you want in your `~/.gitconfig`:

```
[url "git@example.github.com:example"]
insteadOf = git@github.com:example
insteadOf = https://github.com/example
```

This will dynamically replace any URLs that start with "https://github.com/example" or "git@github.com:example" with "git@example.github.com:example". This has the added benefit of letting you `git clone` the URL you would put in your browser to visit a repository on github, but git will automatically use SSH instead of trying HTTP authentication.

Everything should work as before, except git will use the correct SSH key. The only caveat here is that if you have keys in your ssh-agent, but not the one needed to work with the github organisation, your SSH client may not be smart enough to figure that out.
