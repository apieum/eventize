
================
Advanced Usage
================



----------------------------------
Observers inheritance:
----------------------------------

Eventize heavily uses Descriptors, which in python don't know their owner until a getter is called.
Yet, as they help to define classes, it could be interesting to bind them to their class at class creation.

It's the aim of Subject decorator. A Subject is a class that contains descriptors handlers (on_get, before...)

Subject does 2 things:
  * it makes children handlers inheriting their parent handlers observers (parent handlers are found by their attribute name).
  * it calls method handler.bind (if exists) with the owner class as an argument while class is declared.

Subject decorator searches only for types of descriptors given when instanciating events.Subject class.

You can create your own subjects with *"events.Subject([descriptor_type1, [...]])"*.

Eventize comes with already built Subjects for Attributes and Method:

**Attribute Subject** (*attribute.Subject*) is equivalent to *events.Subject(OnGetHandler, OnSetHandler, OnDelHandler, OnChangeHandler)*

**Method Subject** (*method.Subject*) is equivalent to *events.Subject(BeforeHandler, AfterHandler)*

.. code-block:: python

    from eventize import Attribute
    from eventize.attribute import Subject, OnSetHandler

    def validate_string(event):
        if isinstance(event.value, type('')): return

        message = "%s.%s must be a string!" % (type(event.subject).__name__, event.name)
        raise TypeError(message)

    # an observer
    def titlecase(event):
        event.value = event.value.title()

    # user defined attribute with preloaded observer
    class StringAttribute(Attribute):
        on_set = OnSetHandler(validate_string)

    # @Subject with StringAttribute inheritance is equivalent to
    # resetting on_get, on_del... + defining:
    # on_set = OnSetHandler(validate_string, titlecase)
    @Subject  # Bind handlers to the class
    class Name(StringAttribute):
        on_set = OnSetHandler(titlecase)

    assert titlecase not in StringAttribute.on_set
    assert titlecase in Name.on_set

    class Person(object):
        name = Name('john doe')

    john = Person()

    validation_fails = False
    try:
        john.name = 0x007
    except TypeError:
        validation_fails = True

    assert validation_fails, "Validation should fail"
    assert john.name == 'John Doe'  # Name is set in title case



**Remember** when inheriting a Method or Attribute descriptor if you don't override each event handler (on_get, on_set, before...) they are parent's ones.
That's where *Subject* comes handy.

.. code-block:: python

    from eventize import Attribute

    def titlecase(event):
        event.value = event.value.title()

    class Name(Attribute):
        """nothing new"""

    # when doing this:
    Name.on_set.do(titlecase)
    # all classes which use Attribute will have titlecase callback
    assert titlecase in Attribute.on_set
    # because without Subject:
    assert Name.on_set is Attribute.on_set


