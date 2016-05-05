# When to use repositories?
pubdate: 2013-09-30 12:00:00 +0100
tags: Laravel, PHP, Code design

Repositories have their place in applications that deal with fetching stuff - either if it's from a database or an external source. In the Laravel world the repository pattern has been praised a bit too much for its advantages in terms of testability and architecture. I've written about how you can achieve the same level of testability without repositories, but sometimes repositories really are recommended.

A lot of articles about the repository pattern mix in stuff that doesn't have with repositories to do at all like PSR-0 autoloading and dependency injection, which I won't go into depth in this article.

Let's assume you have a controller that's being bogged down with logic. You have several query builders, some spanning as much as 10 lines. This sort of thing does not belong in the controller and is generally making it hard to navigate the source code. Let's take action by moving it all into a third class that lies between the models and the controller - a repository.

A repository class is just a pure class. It doesn't need to extend anything, it's just a collection of functions really. A lot of tutorials will have you creating an interface for the repository - this is absolute nonsense unless you're writing a package for distribution or are writing a database-agnostic app (99% chance you aren't) - so all we're going to do is create a new file named `ThingRepository.php` and stick it somewhere that's being autoloaded by composer.

If you don't know how to do this - make a new folder inside app, let's name it repositories. Put the repository PHP file there. Next, open composer.json and look for the list of classmap autoloaded directories like app/models and app/controllers. Add app/repositories to this list and run `composer dump` (short for dump-autoload) from the command line. You'll need to do this every time you add or rename a class to this directory.

	class ThingRepository
	{
		public function getAllThings()
		{
			return MyModel::all();
		}
	}

Obviously this is a very simple example, but you can easily imagine how to create your own functions that "hide" your 10 line long query builders from the controller. Now, let's utilize this class in our controller.

	class MyController extends Controller
	{
		public function index()
		{
			$repository = new ThingRepository;
			$things = $repository->getAllThings();
			return View::make('myview', ['things' => $things]);
		}
	}

And this will work! It's a little ugly though - we have to instantiate a new ThingRepository in every function. Let's store it on the class.

	class MyController extends Controller
	{
		protected $repo;
	
		public function __construct()
		{
			$this->repo = new ThingRepository;
		}
	
		public function index()
		{
			$things = $this->repo->getAllThings();
			return View::make('myview', ['things' => $things]);
		}
	}

You could also utilize dependency injection if you want! This makes the code more testable and flexible for a variety of reasons I won't go into in depth because this post is about repositories and the benefit they give!

	class ThingRepository
	{
		protected $model;
		
		public function __construct(MyModel $model)
		{
			$this->model = $model;
		}
		
		// ...
	}
	
	class MyController extends Controller
	{
		protected $repo;
			
		public function __construct(ThingRepository $repo)
		{
			$this->repo = $repo;
		}
		
		// ...
	}

And there you have it. No need for PSR-0 autoloading, namespacing or dependency injection if you don't want. Repository classes are not magic and are fairly simple when you get down to the core of it.

Check out a neat base repository class you can use [here](https://github.com/anlutro/laravel-4-base/blob/master/src/anlutro/L4Base/EloquentRepository.php)!