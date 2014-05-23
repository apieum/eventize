********
Eventize
********

.. image:: https://pypip.in/v/eventize/badge.png
        :target: https://pypi.python.org/pypi/eventize


Listen methods "before" and "after" events and attributes "on_get", "on_change", "on_set", "on_del" events.

Features:
  - Easy to use subject/observer pattern
  - Conditionnal events within arguments, values, types... or user defined functions.
  - Attributes support events: "on_get", "on_change","on_set", "on_del"
  - Methods support events "before" and "after"
  - Precise callbacks inheritance (see Subject)
  - Statically and dynamically customizable (via inheritance, visitors, decorators...)

Can listen for events at 3 levels (by order of execution):
  - Descriptor Class: for all Attribute or Method types
  - Descriptor Instance: for all classes that have an Attribute or a Method
  - Object instance: for the given object attribute value or method


---------------------------------------------------------------------

**Table of Contents**


.. contents::
    :local:
    :depth: 1
    :backlinks: none


=============
Installation
=============

Install it from pypi::

  pip install eventize

or from sources::

  git clone git@github.com:apieum/eventize.git
  cd eventize
  python setup.py install

=====
Usage
=====

-------------------------------------------------
Example 0 - as a simple subject/observer pattern:
-------------------------------------------------
**events.Handler is the base class of all eventize handlers ("on_get", "before"...)**

It is a simple callable list of functions wich receive the argument (of type *events.Event*) you've passed when calling your *Handler* object.


As a list an *Handler* support common methods *"append"*, *"remove"*, *"prepend"*, *"insert"*, *"extend"*, *"empty"*..., *"__setitem__"*, plus some syntatic sugar like *"__iadd__"* (+=) for append and *"__isub__"* (-=) for remove.

You can stop event propagation by raising an *events.StopPropagation* exception which store exception message in *"Event.messages"* by default.

You can hook event propagation by overriding methods *"before_propagation"* and *"after_propagation"* or dynamically change *Handler* behaviour at creation by passing visitors (object with a method *"visit"*) see *events.EventType* visitor for example.

An handler can build its proper events of the class defined in *Handler.event_type* when calling *Handler.make_event* (just create and returns an event instanciated with given arguments) or *Handler.notify* (create event with *make_event* and propagates it)

You can add conditionnal handlers by using method *"when"* or restrict the current handler execution by passing *"condition"* kwarg argument to constructor.
Conditions can be chained with methods *"do"* or *"then"* (aliases of *"append"*)

Each time you trigger an event, it is stored in *Handler.events*. You can empty past events by calling *"clear_events"* or all (events and callbacks) with *"clear"*.

.. code-block:: python

  from eventize.events import Handler
  def is_string(event):
    return isinstance(event.content, str)

  def titlecase(event):
    event.content = event.content.title()

  class WeirdVisitor(object):
    def visit(self, handler):
      handler.prepend([self.save_default])

    def save_default(self, event):
      self.default = event.content

  my_visitor = WeirdVisitor()
  handler = Handler(titlecase, my_visitor, condition=is_string)

  # An Handler is a callable list
  assert isinstance(handler, list)
  assert callable(handler)

  # handler contains 2 callbacks:
  assert len(handler) == 2
  assert titlecase in handler
  assert my_visitor.save_default in handler
  # it remove titlecase
  handler -= titlecase
  assert titlecase not in handler
  # it adds titlecase
  handler += titlecase


  # Create event with attribute content and trigger it
  event1 = handler.notify(content="a string")

  assert my_visitor.default == "a string"
  assert event1.content == "A String"

  # if event.content is not a string propagation is stopped
  # these 2 lines are sames as notify
  event2 = handler.make_event(content=1234)
  handler(event2)

  assert len(handler.events) == 2
  assert handler.events == [event1, event2]
  expected_message = "Condition '%s' for event 'Event' return False" % id(is_string)
  assert event2.messages[0] == expected_message

  # we remove all past events:
  handler.clear_events()
  assert len(handler.events) == 0

  # we remove all callbacks and events:
  handler.clear()
  assert len(handler) == 0

  is_a_name = lambda event: event.content == "a name"
  # create a new subhandler with a condition:
  handler.when(is_a_name).do(my_visitor.save_default).then(titlecase)
  event1 = handler.notify(content="a name")
  event2 = handler.notify(content="a string")
  # only "a name" is titlecased
  assert event1.content == "A Name"
  assert event2.content == "a string"

  # save_default is called only for event1:
  assert my_visitor.default == "a name"



-----------------------------
Example 1 - observe a method:
-----------------------------
For compatibility with older versions there is a decorator named "Method" wich returns a method with "before" and "after" properties.
Function "handle" provides a similar result except you can specify the handler type as optionnal third argment.
It's simpler to use directly functions "handle", "before", and "after" as shown here.

.. code-block:: python

  from eventize import before, after
  from eventize.events import Expect

  class Observed(object):
    def __init__(self):
      self.valid = False
      self.logs=[]

    def is_valid(self, *args):
      return self.valid

    def not_valid(self, event):
      # can do:
      # event.subject.valid = not event.subject.valid
      # equivalent to
      self.valid = not self.valid

  class Logger(list):
    def log_before(self, event):
      self.append(self.message('before', *event.args, is_valid=event.subject.valid))

    def log_after(self, event):
      self.append(self.message('after', *event.args, is_valid=event.subject.valid))

    def message(self, event_name, *args, **kwargs):
      return "%s called with args: '%s', current:'%s'" % (event_name, args, kwargs['is_valid'])



  my_object = Observed()
  my_logs = Logger()
  called_with_permute = Expect.arg('permute')

  before_is_valid = before(my_object, 'is_valid')
  before_is_valid += my_logs.log_before
  before_is_valid.when(called_with_permute).do(my_object.not_valid)
  after(my_object, 'is_valid').do(my_logs.log_after)

  assert my_object.is_valid() is False
  assert my_object.is_valid('permute') is True

  assert my_logs == [
    my_logs.message('before', is_valid=False),
    my_logs.message('after', is_valid=False),
    my_logs.message('before', 'permute', is_valid=False),
    my_logs.message('after', 'permute', is_valid=True),
  ]


---------------------------------
Example 2 - observe an attribute:
---------------------------------
Like for methods, you can still use "ObservedAttribute" to declare directly an attribute (see ex. 4) or to decorate an attribute.
New api at version 0.3.1, provides "handle", "on_get", "on_set" and "on_del" functions to add events on attributes.
As I had to provide 'on_set', 'on_get', 'on_del' on object instance observed attributes, each times you were setting an observed attribute, its value was replaced by a wrapper which causes matters for constants like booleans or None (ex 3).
This behaviour will be removed soon (version 0.4) so prefer use new api which will hide all this mecanic.

.. code-block:: python


  from eventize import handle
  class Validator(object):
    def __init__(self, is_valid):
      self.valid = is_valid

    def __call__(self):
      return self.valid

  class Observed(object):
    validate = Validator(False)

  class Logger(list):
    def log_get(self, event):
      self.append(self.message('on_get', event.name, event.value.valid))
    def log_set(self, event):
      self.append(self.message('on_set', event.name, event.value.valid))
    def log_del(self, event):
      self.append(self.message('on_del', event.name, event.value.valid))

    def message(self, event_name, attr_name, value):
        return "'%s' called for attribute '%s', with value '%s'" % (event_name, attr_name, value)

  my_object = Observed()
  my_logs = Logger()
  # Note: order matter here !
  my_object_validate = handle(my_object, 'validate')
  my_object_validate.on_del += my_logs.log_del
  my_object_validate.on_set += my_logs.log_set
  my_object_validate.on_get += my_logs.log_get

  Observed_validate = handle(Observed, 'validate')
  Observed_validate.on_set += my_logs.log_set
  Observed_validate.on_del += my_logs.log_del
  Observed_validate.on_get += my_logs.log_get

  assert my_object.validate() == False, 'Default value was not set'
  setattr(my_object, 'validate', Validator(True))
  del my_object.validate

  assert my_logs == [
    my_logs.message('on_get', 'validate', False),  # Called at class level
    my_logs.message('on_get', 'validate', False),  # Called at instance level
    my_logs.message('on_set', 'validate', True),   # Called at class level
    my_logs.message('on_set', 'validate', True),   # Called at instance level
    my_logs.message('on_del', 'validate', True),   # Called at class level
    my_logs.message('on_del', 'validate', True),   # Called at instance level
  ]



-----------------------------------------------------------
Example 3 - observe an attribute for non overridable types:
-----------------------------------------------------------

Note (will change soon):
  If can't set attributes (when setattr fails for on_get) to Attribute value

  -> Handler try to subtype value.

  If value can't be subtyped (for non overridable type like None, Booleans...)

  -> Handler returns value as is.

  This means you can't call on_get, on_set, or on_del on instance.


  Yet, you can do this at class level, with handler conditional method 'when'


  For more information about Expect and how it functions have a look at inxpect package: https://pypi.python.org/pypi/inxpect


.. code-block:: python

  from eventize import on_set
  from eventize.events import Expect

  class Observed(object):
    valid = False

  class Logger(list):
    def log_set(self, event):
      self.append(self.message('on_set', event.name, event.value))

    def log_set_error(self, event):
      self.append(self.message('on_set_error', event.name, event.value))

    def message(self, event_name, attr_name, value):
      return "'%s' called for attribute '%s', with value '%s'" % (event_name, attr_name, value)

  my_object = Observed()
  other_object = Observed()
  my_logs = Logger()

  dont_change_value = lambda event: setattr(event, 'value', event.subject.valid)
  value_is_not_bool = Expect.value.type_is_not(bool)
  subject_is_my_object = Expect.subject(my_object)

  getting_my_object = on_set(Observed, 'valid').when(subject_is_my_object)
  getting_my_object += my_logs.log_set  # (1)
  getting_my_object.when(value_is_not_bool).do(my_logs.log_set_error).then(dont_change_value)  # (2)

  my_object.valid = True  # (1)
  my_object.valid = None  # (2)
  other_object.valid = True  # Trigger no event
  other_object.valid = None  # Trigger no event

  assert my_object.valid == True  # (2) -> dont_change_value

  assert my_logs == [
    my_logs.message('on_set', 'valid', True),
    my_logs.message('on_set', 'valid', None),
    my_logs.message('on_set_error', 'valid', None),
  ]



----------------------------------
Example 4 - Observers inheritance:
----------------------------------
Descriptors in python don't know their owner until a getter is called.
Yet, as they help to define classes, it could be interesting to bind them to their class at class creation.

It's the aim of Subject decorator. A Subject is a class that contains descriptors handlers (on_get, before...)

Subject make 2 things:
  * it makes children handlers inheriting their parent handlers observers (parent handlers are found by their attribute name).
  * it calls method handler.bind (if exists) with the owner class as an argument while class is declared.


Here we'll see only how observers inheritance is done.


.. code-block:: python

  from eventize import attribute, Attribute

  def validate_string(event):
    if isinstance(event.value, type('')): return

    message = "%s.%s must be a string!" % (type(event.subject).__name__, event.name)
    raise TypeError(message)

  def titlecase(event):
    event.value = event.value.title()

  class StringAttribute(Attribute):
    on_set = attribute.Handler(validate_string)

  @attribute.Subject  # Bind handlers to the class -> this is the way inheritance is done
  class Name(StringAttribute):
    on_set = attribute.Handler(titlecase)

  class Person(object):
    name = Name('doe')

  john = Person()

  validation_fails = False
  try:
    john.name = 0x007
  except TypeError:
    validation_fails = True

  assert validation_fails, "Validation should fail"
  assert john.name == 'Doe'  # Name is auto magically set in title case



----------------------------------
Example 5 - Choose your handler:
----------------------------------
Illustrate the use of the third optionnal argument of "handle", "on_get", "on_set", "on_del", "before" and "after"

.. code-block:: python

  from eventize import method, Method
  from eventize import before

  def first_arg_is_string(event):
    if isinstance(event.args[0], type('')): return
    raise TypeError("First arg must be a string!")

  def titlecase(event):
    # args are a tuple
    args = list(event.args)
    args[0] = args[0].title()
    event.args = tuple(args)

  class FirstArgIsStringMethod(Method):
    before = method.Handler(first_arg_is_string)

  class Person(object):
    def __init__(self, name):
      self.set_name(name)

    def set_name(self, name):
      self.name = name

  # calling before with FirstArgIsStringMethod
  before(Person, 'set_name', FirstArgIsStringMethod).do(titlecase)

  validation_fails = False
  try:
    Person(0x007)
  except TypeError:
    validation_fails = True


  john = Person("john doe")

  assert validation_fails, "Validation should fail"
  assert john.name == 'John Doe'  # Name is auto magically set in title case




===========
Development
===========

Your feedback, code review, improvements or bugs, and help to document is appreciated.
You can contact me by mail: apieum [at] gmail [dot] com

Test recommended requirements::

  pip install -r dev-requirements.txt


Launch test::

  git clone git@github.com:apieum/eventize.git
  cd eventize
  nosetests --with-spec --spec-color ./
  # or with watch
  # nosetests --with-spec --spec-color --with-watch ./




.. image:: https://secure.travis-ci.org/apieum/eventize.png?branch=master
   :target: https://travis-ci.org/apieum/eventize
