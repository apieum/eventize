
================
Advanced Usage
================



----------------------------------
Observers inheritance:
----------------------------------

Eventize heavily uses Descriptors, which in python don't know their owner until a getter is called.
Yet, as they help to define classes, it could be interesting to bind them to their class at class creation.

It's the role of events.Subject instances wich build Subject decorators.

Subject decorators does 2 things:
  * it makes children handlers inheriting their parent handlers observers (parent handlers are found by their attribute name).
  * it calls method handler.bind (if exists) with the owner class as an argument while class is declared.

They searches only for types of descriptors given when instanciating events.Subject class.

You can create your own subjects with *"events.Subject([descriptor_type1, [...]])"*.

Eventize comes with already built in Subjects for Attributes and Method:

**Attribute Subject** (*attribute.Subject*) is equivalent to *events.Subject(OnGetHandler, OnSetHandler, OnDelHandler, OnChangeHandler)*

**Method Subject** (*method.Subject*) is equivalent to *events.Subject(BeforeHandler, AfterHandler)*

.. literalinclude:: ../../tests/examples/inheritance1.py
   :caption: tests/examples/inheritance1.py
   :name: inheritance1


**Remember** when inheriting a Method or Attribute descriptor if you don't override each event handler (on_get, on_set, before...) they are parent's ones.
That's where *Subject* comes handy.

.. literalinclude:: ../../tests/examples/inheritance2.py
   :caption: tests/examples/inheritance2.py
   :name: inheritance2

