# Laravel and SemVer

There's been some discussion around Laravel and SemVer (semantic versioning) recently, which I appreciate. SemVer is in my eyes a very important guideline for frameworks and widely adopted libraries.

A major concern when picking frameworks is, am I going to get security and feature upgrades without risking breaking my application? In laravel, you currently don't. Each minor version (4.1, 4.2, 4.3) has introduced breaking changes - there have even been breaking changes in "bugfix" versions because new features are introduced here.

In addition to this, critical bugfixes are not being backported to older minor versions of the framework, so if you want to stay secure you pretty much have to upgrade.

Maybe this isn't a problem for a lot of people, but my experience is that in Laravel, a lot of things are hard coded, so for large applications with specific needs you often need to extend core classes. This makes the application more likely to break when you upgrade, and requires more time to fix.

If you're building a large application you also likely have your own sort of framework built on top of Laravel again, maybe you're depending on packages specific to Laravel - these are a lot of points that are vulnerable to breaking.

In fact, as a package maintainer myself, I often have to consider if I need to ditch the generic "~4.1" version constraint and exclude the specific minor versions that I know don't work 100% with the package.

Following semver makes it easier to catch bugs and problems that aren't catchable with regular unit tests. If your new minor version requires an hour's work or so to upgrade, and potentially break existing functionality (sometimes on purpose), few people are going to want to beta test that. If instead you make the promise that "change the version constraint in your composer.json - you won't have to change anything in your code, and if you do, it's a bug" a lot more people would be open to beta testing, I think.

If Laravel were to use semver, it shouldn't do so "just because". You would have to either release a new major version every time you make a breaking change, exposing how volatile the framework really is, or make an effort to make less breaking changes, enforcing new features to only be introduced in minor versions and bugfixes in bugfix versions. While following semver 100% is practically impossible, making a dedicated effort in that direction would make a welcome change.