# Assertions on mails in Laravel 4
pubdate: 2014-07-05 12:00:00

Testing mails in Laravel 4 is a bit of a weak spot. You can say `Mail::shouldReceive('send')->once()...` but specifying everything the method should receive in terms of arguments as well as asserting that the closure sets the recipient and subject correctly is tedious at best. [This SO answer](http://stackoverflow.com/questions/18406497/how-to-test-mail-facade-in-laravel-4/18431205#18431205) shows an example of how to unit test a mail being sent.
pubdate: 2014-07-05 12:00:00

There is a better way, as long as you're doing functional testing - that is, extending the TestCase that comes with Laravel and doing `$this->call(...)` stuff. We mock one layer deeper, the SwiftMailer service, and gain access to more rich information.

First of all, we swap the swiftmailer instance on the IoC container.

    $mock = Mockery::mock('Swift_Mailer');
    $this->app->make('mailer')->setSwiftMailer($mock);

Second, we define its expectations, and use Mockery's `andReturnUsing` to run assertions on the method call.

    $mock->shouldReceive('send')->once()
      ->andReturnUsing(function($msg) {
        // assert stuff here
      });

$msg above is an instance of Swift_Message, a class which API is buried deep within the SwiftMailer class hierarchy, but I'll show the most important ones here.

    $this->assertEquals('My subject', $msg->getSubject());
    $this->assertEquals('foo@bar.com', $msg->getTo());
    $this->assertContains('Some string', $msg->getBody());

If you're sending an email that is both HTML and plain text, you may want to get both the regular HTML body as well as the plain text one.

    $htmlBody = $msg->getBody();
    $children = $msg->getChildren();
    $plainBody = $children[0]->getBody();

This should allow you to write shorter, more accurate and realistic tests.