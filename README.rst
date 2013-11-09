********
Eventize
********

.. image:: https://pypip.in/v/eventize/badge.png
        :target: https://pypi.python.org/pypi/eventize


Add events to object methods and attributes.

Events are triggered at 3 levels in order:
  * Descriptor Class: for all Attribute or Method types (from version 0.3)
  * Descriptor Instance: for all classes that have an Attribute or a Method
  * Object instance: for the given object attribute value or method


Methods support events "before" and "after"
Attributes support events: "on_get", "on_set", "on_del"

Events can be triggered conditionaly within arguments or user condition.

Since version 0.3, observers defined at Descriptor Instance level are preserved in descriptor container class children, providing inheritance. see example 4

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

-----------------------------
Example 1 - observe a method:
-----------------------------
  As ObservedMethod class take a function as argument it can be used as a decorator.

.. code-block:: python


  from eventize import ObservedMethod
  from eventize.events import Expect

  class Observed(object):
    def __init__(self):
      self.valid = False
      self.logs=[]

    @ObservedMethod
    def is_valid(self, *args, **kwargs):
      return self.valid

    def not_valid(self, event):
      event.subject.valid = not event.subject.valid

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

  my_object.is_valid.before += my_logs.log_before
  my_object.is_valid.before.when(called_with_permute).do(my_object.not_valid)
  my_object.is_valid.after += my_logs.log_after

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

.. code-block:: python

  from eventize import ObservedAttribute
  class Validator(object):
    def __init__(self, is_valid=False):
      self.valid = is_valid

  class Observed(object):
    validator = ObservedAttribute(default=Validator(False))

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
  my_object.validator.on_del += my_logs.log_del
  my_object.validator.on_set += my_logs.log_set
  my_object.validator.on_get += my_logs.log_get

  Observed.validator.on_set += my_logs.log_set
  Observed.validator.on_del += my_logs.log_del
  Observed.validator.on_get += my_logs.log_get

  assert my_object.validator.valid == False, 'Default value was not set'
  setattr(my_object, 'validator', Validator(True))
  del my_object.validator

  assert my_logs == [
    my_logs.message('on_get', 'validator', False),  # Called at class level
    my_logs.message('on_get', 'validator', False),  # Called at instance level
    my_logs.message('on_set', 'validator', True),   # Called at class level
    my_logs.message('on_set', 'validator', True),   # Called at instance level
    my_logs.message('on_del', 'validator', True),   # Called at class level
    my_logs.message('on_del', 'validator', True),   # Called at instance level
  ]



-----------------------------------------------------------
Example 3 - observe an attribute for non overridable types:
-----------------------------------------------------------

Note:
  If can't set attributes (when setattr fails for on_get) to Attribute value

  -> Handler try to subtype value.

  If value can't be subtyped (for non overridable type like None, Booleans...)

  -> Handler returns value as is.

  This means you can't call on_get, on_set, or on_del on instance.


  Yet, you can do this at class level, with handler conditional method 'when'


  For more information about Expect and how it functions have a look at inxpect package: https://pypi.python.org/pypi/inxpect


.. code-block:: python


  from eventize import ObservedAttribute
  from eventize.events import Expect

  class Observed(object):
    valid = ObservedAttribute(False)

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

  subject_is_my_object = Expect.subject(my_object)

  getting_my_object = Observed.valid.on_set.when(subject_is_my_object)
  getting_my_object += my_logs.log_set  # (1)

  dont_change_value = lambda event: setattr(event, 'value', event.subject.valid)
  value_is_not_bool = Expect.value.type_is_not(type(False))
  getting_my_object.when(value_is_not_bool).do(my_logs.log_set_error).then(dont_change_value)  # (2)

  my_object.valid = True  # call (1)
  my_object.valid = None  # call (2) -> dont_change_value
  other_object.valid = True  # Trigger no event
  other_object.valid = None  # Trigger no event

  assert my_object.valid == True

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


  from eventize.attribute import Attribute, AttributeHandler, AttributeSubject

  def validate_string(event):
    if isinstance(event.value, type('')): return

    message = "%s.%s must be a string!" % (type(event.subject).__name__, event.name)
    raise TypeError(message)

  def titlecase(event):
    event.value = event.value.title()

  class StringAttribute(Attribute):
    on_set = AttributeHandler(validate_string)

  @AttributeSubject  # Bind handlers to the class -> this is the way inheritance is done
  class NameAttribute(StringAttribute):
    on_set = AttributeHandler(titlecase)

  class Person(object):
    name = NameAttribute('doe')

  john = Person()

  validation_fails = False
  try:
    john.name = 007
  except TypeError:
    validation_fails = True

  assert validation_fails
  assert john.name == 'Doe'  # Name is auto magically set in title case



===========
Development
===========

Your feedback, code review, improvements or bugs, and help to document is appreciated.
You can contact me by mail: apieum [at] gmail [dot] com


Launch test::

  git clone git@github.com:apieum/eventize.git
  cd eventize
  nosetests --with-spec --spec-color ./




.. image:: https://secure.travis-ci.org/apieum/eventize.png?branch=master
   :target: https://travis-ci.org/apieum/eventize
