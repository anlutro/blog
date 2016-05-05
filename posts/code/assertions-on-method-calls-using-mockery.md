# Assertions on method calls using Mockery
pubdate: 2013-08-20 12:00:00 +0100
tags: Mockery, PHP

I had a problem recently where I wanted to use PHPUnit to test what was being passed to a function. We're talking about a several hundred line string with a current timestamp, so simply using `$mock->shouldReceive('method')->with('parameter string')` wouldn't work.

One option would be to write a mock implementation of the class that should receive the method call which stores the method parameter in a public variable on the class and then do the assertions on that, but I usually try to avoid solutions like that - especially when it's just for doing simple assertions on a string.

The first solution I found was using Mockery's **andReturnUsing** method, which passes the parameters passed to the method on to a closure. The following works in PHP 5.4 or later:

	$this->logger->shouldReceive('error')->once()
		->andReturnUsing(function($logged) {
			$this->assertContains('Route: action', $logged);
			$this->assertContains('URL: url', $logged);
		});

The problem with this is that you can't chain andReturnUsing with a normal andReturn method - meaning if the method call should return anything, it needs to do so inside the closure. This can be problematic if you want to check the method call parameters in the same way multiple places but return different values - with andReturnUsing you'd have to redefine the same closure over and over again, only changing the return statement.

A little research revealed that the Mockery::on function is what I'm looking for:

	$this->logger->shouldReceive('error')->once()
		->with(Mockery::on(function($logged) {
			$this->assertContains('Route: action', $logged);
			$this->assertContains('URL: url', $logged);
			return true;
		}));

If closure you pass to Mockery::on should returns false, you'll get a `Mockery\\Exception\\NoMatchingExpectationException: No matching handler found for class::method` exception. We don't really care about that, the assertions will do what we want and tell us if something is wrong.

This way, you can even call a closure on a specific parameter while simply leaving the other parameters as variables as you normally would - and you can add `->andReturn` at the end of the chain.

However, using $this in a closure doesn't work in PHP 5.3 and older. For that, you need to use a **reference** to an outside variable which we will then later do assertions on.

	$this->logger->shouldReceive('error')->once()
		->with(Mockery::on(function($input) use(&$logged) {
			$logged = $input;
			return true;
		}));
	
	$this->handler->handleException($exception);
	
	$this->assertContains('Route: action', $logged);
	$this->assertContains('URL: url', $logged);

Notice how we had to delay the assertions until after the event chain has been triggered (in this case, I was testing an exception handler) - you can't assert on $logged until the closure has actually been invoked.

An example I posted on StackExchange, testing mails in Laravel 4: [http://stackoverflow.com/a/18431205/2490608](http://stackoverflow.com/a/18431205/2490608)