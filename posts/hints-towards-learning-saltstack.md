# Hints towards learning SaltStack
pubdate: 2015-06-28 00:19:38

SaltStack is an awesome provisioning tool I've adapted in the past few months. I'd like to share a few pointers to other people working with it for the first time.

**Know Python.** A lot of Jinja logic will borrow heavily from Python, and to best understand a lot of Salt's inner workings you need to understand how Python works. You need to know the difference between a dict and a list, and you need to know how to iterate over a dict.

**Understand the data flow.** When you're doing `foo: {{ foo }}` in an SLS file, it's not like passing a variable to a function. Your variable gets cast to a string before it's parsed as YAML. A lot of weird stuff can happen in the process. For example, `foo: {{ 'yes' }}` will result in the python dict `{'foo': True}` because "yes" is a boolean constant in YAML.

**Learn the difference between states and modules.** State functions are the ones you put into your SLS files (pkg.installed, file.managed etc.), module functions are called via `{{ salt['module.function'] }}`. `pillar.get` is a very commonly used module function. When you run `salt '*' state.highstate` you're actually calling the module function `state.highstate`.

**Use formulas as examples, not plugins.** Many of the [SaltStack formulas](https://github.com/saltstack-formulas) are either broken, overcomplicated or just not suitable for your use case. Use them for inspiration and learning, feel free to copy-paste bits from them, but manage your own formulas.

**Consider pillars arguments for your states.** Your states should contain instructions on how things are to be done, pillars are *what* needs to be done. What needs to be done may vary from server to server, but how it's done probably won't. If it does, add pillar entries that specify this varying behaviour (for example, versions of sotftware, whether to compile from source etc.).

**Multiple pillar files can add to the same pillar dict.** You can have foo.sls and bar.sls both adding an element to a dictionary in the pillar, and they'll be merged on compilation. Even works on nested dicts - but does not work with lists!

SaltStack is a fast moving project with a lot of intertwined functionality. Things break quite often, and the code is often quite a mess of patches. Expect there to be bugs, report them on Github.
