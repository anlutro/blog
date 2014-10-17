# Shrinking controllers and abstracting with manager classes

There are a lot of articles revolving around Laravel 4 specifically that try and explain how to abstract logic away from your controller, but most of them either kinda miss the point or overcomplicate things (by using facades, repositories, interfaces...).

The only thing you need to know before following this guide is how to create your own custom classes and make composer autoload them. This is a fairly simple thing to do which I won't cover here.

The simplest way to abstract logic away from your controllers is to grab all the logic that isn't directly tied to any of these things:

1. Fetching input (`Input::all()`)
2. Returning a response (usually a redirect or a view)
3. Putting stuff into the session (flash messages)

Everything else - validation, mail, queue and database stuff - you should copy into a class called a manager. If your controller is called `ThingController,` your manager should be called `ThingManager`. Do not worry about using static method calls and facades within the manager class - our main focus for now is to move business logic away from the controller.

Once the manager class has been made, inject it into the controller simply by typehinting the constructor argument. Laravel's IoC container takes care of the rest for us. Now, we can call our manager's methods within the controller - for example, `$this->thingManager->myMethod(Input::all())` and do something with what is returned. For example, we may redirect to two different URLs depending on whether it returned true or false.

Here's [an example](https://gist.github.com/anlutro/26d630d0b573e69a7ca1) of what a refactored controller might look like.