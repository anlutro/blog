# Using the Form Builder as little as possible
pubdate: 2013-10-05 12:00:00

I love the Laravel 4 FormBuilder (accessible through the `Form::` facade) - automatic re-populating of input from the session and from a model is awesome. In the upcoming versions you will even be able to use accessors to populate form fields from the model even if they're not actually fields in the database.

However, sometimes (especially when using a stylesheet framework) it can be hard to get the markup to behave as you want when constructing a form. If you want to construct the HTML for an input yourself but still reap the benefits of automatic repopulation from session/model, there is the function `getValueAttribute` which lets you get the value of a certain input in your form either from the session or the model.

	{{ Form::model($model, ['class' => 'form-horizontal', 'role' => 'form']) }}

	<input type="text" name="my_field" value="{{ Form::getValueAttribute('my_field', 'Default') }}" />

	{{ Form::close() }}

Make sure the input name attribute and the key you use for `getValueAttribute` match. We still need to use `Form::model` if we want population from a model, but a `Form::open` can easily be replaced with normal HTML as well. Keep in mind the priority of data when forms are populated - session comes before 'Default' which again comes before model data.