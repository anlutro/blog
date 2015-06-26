# Testable, simple L4 code without repository patterns
pubdate: 2013-08-31 12:00:00

There's a lot of people advocating the repository pattern for testability in your Laravel 4 projects. Fact is, it doesn't make your code that much more testable, and you can easily achieve the same level of testability by using your models as you would a repository.

First of all, let me say that repositories are very handy if you find yourself either chaining tons of query builder function calls in your controller, or defining a lot of static functions on your models. A repository can then be a handy layer between your controllers and models which gathers all that clutter into one class, where you can name your functions something like searchAndFilterWithRelatedModels.

I'm not a huge fan of the pattern and you can probably find others who can argue for it better than me...

Anyway, on to my main point. The point that many people have been making is that by injecting a repository into your controllers, you gain testability because you can swap out the repository with a mock. Unless you're using something extremely high-tech like AspectMock to intercept function calls, you won't be able to do the same if your controller passes `Post::all()` to your view. What most people don't seem to tell you is that you can do the exact same dependency injection with your models, and in most cases it's a simple search and replace to swap out your static class calls with the new injected method.

Here's a very simple controller example. I've commented out the "old" code.

	class MyController extends Controller
	{
		protected $model;

		public function __construct(MyModel $model)
		{
			$this->model = $model;
		}

		public function index()
		{
			// MyModel::all();
			return View::make('myindex', [
				'models' => $this->model->all()
			]);
		}

		public function show($modelId)
		{
			// MyModel::find($modelId);
			return View::make('myshow', [
				'model' => $this->model->find($modelId)
			]);
		}
	}

The magic that happens here is that Laravel automatically hands the controller an instance of MyModel. You'll see how we can manipulate Laravel into passing it a mock object instead of a real model later on.

The reason we can simply swap `MyModel::` with `$this->model` is because of the way Eloquent models handle static method calls. Every static method call on a model basically spins up a new instance of that model and then does a normal method call on that new instance. There are a few exceptions, but none that should matter in a controller context.

Here is the corresponding test. We'll define the mock in the setUp method as we'll be re-using it practically for every test in the file. Notice how we create a mock object where we can set expectations etc., and then tell Laravel (`$this->app`) to use that instance whenever it's asked for an instance of `MyModel`.

	class MyControllerTest extends TestCase
	{
		public function setUp()
		{
			parent::setUp();
			$this->mockModel = Mockery::mock('MyModel');
			$this->app->instance('MyModel', $this->mockModel);
		}
		
		public function tearDown()
		{
			Mockery::close(); // important when using mockery!
		}

		public function testIndex()
		{
			// return an empty array because our index view has a foreach
			// loop that would error if we returned something non-iterable
			$this->mockModel->shouldReceive('all')
				->once()
				->andReturn([]);

			$this->call('get', '/my-route');

			$this->assertResponseOk();
			$this->assertViewHas('models');
		}

		public function testShow()
		{
			// this is the best way to mock a real model to pass to a
			// view without having to add ->shouldReceive for every
			// single function and defining every single variable on it.
			$mock = Mockery::mock(new MyModel);

			$this->mockModel->shouldReceive('find')
				->once()
				->with(1)
				->andReturn($mock);

			$this->call('get', '/my-route/1');

			$this->assertResponseOk();
			$this->assertViewHas('model');
		}
	}

Maybe there are times when this isn't appropriate - if your controllers use a lot of different models that all need to be injected and there's no way to move those onto relationships, there might be a slight performance loss? I doubt it's big though - and the testability you gain from practically no effort is huge.