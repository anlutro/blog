# Optimizing for production with Laravel 4
pubdate: 2013-08-20 12:00:00 +0100
tags: Laravel

Documentation on optimization and performance is somewhat lacking for Laravel 4 at the moment. In this post I'll give some quick pointers as to how Laravel 4 works and how you can improve its performance.

First of all, realize that the things that apply to normal PHP development also apply to Laravel 4. Built-in PHP functions will be more efficient than trying to do stuff manually, your database layout can and will affect performance and so on.

Laravel uses lazy autoloading for classes. This means that if it doesn't include EVERY file in the vendor directory, but rather waits for a call on a class that hasn't been loaded yet, and then makes some intelligent guesses as to where it might be located. If you're using [PSR-0 autoloading](https://github.com/php-fig/fig-standards/blob/master/accepted/PSR-0.md), it checks for the file Namespace/Namespace/Class.php in the PSR-0 directories you have defined in your composer.json. If you're using classmap, it simply looks up the name of the class and loads the corresponding file. This is why, if you've added a new class to a directory only being autoloaded via classmap, you get "class not found" until you run `composer dump-autoload`.

Laravel 4 adds a few directories to the autoloader on run-time by default. Open app/start/global.php and you'll see a call to `ClassLoader::addDirectories` - classes inside these directories will also be autoloaded using the PSR-0 rule. For performance, you should remove this function call altogether and just rely on Composer's autoloading.

PSR-0 is nice for development because it lets you add a class and it will instantly be found by the autoloader - as long as you've namespaced it correctly and named the file correctly, of course. In production, you usually don't want to use PSR-0 autoloading as it has a bit of overhead. Use `composer dump-autoload --optimize` to re-compile all your PSR-0 autoloading rules into classmap rules, which are faster.

When debug is set to false in app/config/app.php, Laravel's Artisan function `php artisan optimize` will do two things: Run the `composer dump-autoload --optimize` command, as well as generate the file bootstrap/compiled.php. This file contains a lot of the common Laravel framework class files, and allows for the system to just require one file even though the framework is in reality split into many hundreds of files.

Running php artisan optimize every time you update your files is highly recommended as it can increase your performance by a lot. Consider having it done automatically every time you deploy (preferably after a temporary `php artisan down` to prevent issues).

You can add files to this compiled file by adding them to the array in app/config/compile.php. Files should be referenced relative to the project root - for example:

	'vendor/laravel/framework/src/Illuminate/Support/Collection.php',
	'vendor/cartalyst/sentry/src/Cartalyst/Sentry/Sentry.php',
	'app/library/HelperClass.php',

Use a profiler like [loic-sharma/profiler](https://github.com/loic-sharma/profiler) to find out which files are being loaded on your requests and add them to your compiled.php array. I've had my response time almost halved by doing this.

And as a last note - never have workbenches on your production server. There is a lot of overhead related to workbenches, and they should only be used for local development.