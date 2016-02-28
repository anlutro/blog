# Mocking models using Mockery
pubdate: 2014-01-17 12:00:00
tags: Mockery, Laravel

Mocking classes and defining what methods they should receive is easy.

    // MyRepository
    public function getAll()
    {
      return $this->model->get();
    }

    // MyRepositoryTest
    public function testGetAll()
    {
      $model = Mockery::mock('MyModel');
      $repo = new MyRepository($model);
      $model->shouldReceive('get')->once()->andReturn('foo');
      $this->assertEquals('foo', $repo->getAll());
    }

However, what if you want to test a method/class that not only calls method on that class but relies on or sets variables on it? Often you'll find that Mockery throws errors like 'getAttribute does not exist on this mock object'. The answer is simple - use Mockery's partial mocks.

A partial mock is what it sounds like - parts of the class is mocked, but other parts of it is not and functions as the class normally would. In this case we're making a partial mock because we want the attribute setting to work as normal, but we also don't want the real save() method to be called as that would write to our database.

    // MyRepository
    public function updateStuff(MyModel $model)
    {
      if (!$model->exists) throw new Exception;
      if ($this->model->where('foo', '=', $model->foo)->exists()) return false;
      $model->foo = 'foo';
      $model->bar = 'bar';
      return $model->save();
    }

    // MyRepositoryTest
    public function testUpdateSomeStuff()
    {
      $model = Mockery::mock('MyModel');
      $model->shouldReceive('where->exists')->andReturn(false);
      $repo = new MyRepository($model);
      $model = Mockery::mock('MyModel')->makePartial();
      $model->shouldReceive('save')->once()->andReturn(true);
      $model->exists = true;
      $this->assertTrue($repo->updateStuff($model));
      $this->assertEquals('foo', $model->foo);
      $this->assertEquals('bar', $model->bar);
    }

It is worth noting that in clean OOP it is better to simply wrap the logic shown in updateStuff in a method on the model and make the repository use that, but I'll leave it as is for the sake of this example. Partial mocks are useful in other places than this - sometimes you may want to send a partial mock to a view to test the view, sometimes it may be more work to mock out a method of a class than let it do its normal thing.

Partial mocks should in general be avoided when possible. If you need a lot of partial mocks in your tests it might be an indication that your classes are doing too much, and every time you make a partial mock to inject into another class you can not easily be confident that the two classes are only loosely decoupled. That being said, they are an extremely powerful tool - but use them with caution.