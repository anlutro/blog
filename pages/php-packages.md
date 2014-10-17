# My PHP packages

**Autarky** - [https://github.com/autarky/framework](https://github.com/autarky/framework)

Framework built from scratch utilizing community packages and best practices.

**Menu** - [https://github.com/anlutro/php-menu](https://github.com/anlutro/php-menu)

Dynamic menu builder with support for multiple menus, submenus, classes, glyphicons and font awesome icons.

**Form** - [https://github.com/anlutro/php-form](https://github.com/anlutro/php-form)

Designed as a sort of hybrid between Laravel's and Symfony's form builder. Functionality for validation, input transformation, casting checkboxes to booleans and much more.

## Laravel 4-specific

**Laravel 4 Smart Errors** - [https://github.com/anlutro/laravel-4-smart-errors](https://github.com/anlutro/laravel-4-smart-errors)

Send yourself emails with exception information and alert-level logs, more detailed default logging, a default CSRF and 404 handler and more. Useful for small apps or if you in general don't want to invest in something more sophisticated like bugsnag.

**Laravel Repository** - [https://github.com/anlutro/laravel-repository](https://github.com/anlutro/laravel-repository)

Eloquent and query builder implementations of the repository pattern. Definitely not as "clean" as a pure implementation such as doctrine, but adds functionality and might help you keep your code more DRY.

**Laravel Validation** - [https://github.com/anlutro/laravel-validation](https://github.com/anlutro/laravel-validation)

Abstract class that wraps laravel's validator and allows you to dynamically add/remove rules, replace variables in rules, replace placeholders in rules with contents of other inputs, throw detailed exceptions and more.

**Laravel Settings** - [https://github.com/anlutro/laravel-settings](https://github.com/anlutro/laravel-settings)

Persistant settings, shared across your application for all users, stored either in the database or in a JSON file.

**Laravel Testing** - [https://github.com/anlutro/laravel-testing](https://github.com/anlutro/laravel-testing)

Abstract TestCases you can extend from. Includes a test case which is basically the default Laravel one but with extra functionality, as well as a TestCase for testing full-stack apps inside a package, and a database testcase that allows you to run tests against a test database, using Eloquent and the query builder, without needing to boot the entire framework.
