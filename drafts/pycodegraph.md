# pycodegraph
pubdate: 2019-11-22 20:35 CET

In Python, circular imports are generally something I try to avoid. There are two main reasons for this:

1. It can cause bugs. If module A imports module B and module B imports module A and they refer to each other, not all symbols in either module may be defined, and you may get `AttributeError: module 'a' has no attribute 'example'` even though it clearly has that defined.
2. It's a sign of poor code design. Two modules that depend on each other is ...

In a small code base, circular imports may be easy to spot, but as your project grows it can get more difficult. Worse, your circular import may be several levels deep: A imports from B, B from C, C from D, and D from A.

Other languages "solve" this problem by...

However, Python is Python and is likely to stay that way, so I figured I wanted to build a tool to help me spot circular imports.
