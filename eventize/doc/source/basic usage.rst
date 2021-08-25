
============
Basic Usage
============

-------------------------------------------------
Simple subject/observer
-------------------------------------------------
**events.Handler is the base class of all eventize handlers ("on_get", "before"...)**

It is a simple callable list of functions wich receive the argument (of type *events.Event*) you've passed when calling your *Handler* object.


As a list an *Handler* support common methods *"append"*, *"remove"*, *"prepend"*, *"insert"*, *"extend"*, *"empty"*..., *"__setitem__"*, plus some syntactic sugar like *"__iadd__"* (+=) for append and *"__isub__"* (-=) for remove.

You can stop event propagation by raising an *events.StopPropagation* exception which store exception message in *"Event.messages"* by default.

You can hook event propagation by overriding methods *"before_propagation"* and *"after_propagation"* or dynamically change *Handler* behaviour at creation by passing visitors (object with a method *"visit"*) see *events.EventType* visitor for example.

An handler can build its proper events of the class defined in *Handler.event_type* when calling *Handler.make_event* (just create and returns an event instanciated with given arguments) or *Handler.notify* (create event with *make_event* and propagates it)

You can add conditional handlers by using method *"when"* or restrict the current handler execution by passing *"condition"* kwarg argument to constructor.
Conditions can be chained with methods *"do"* or *"then"* (aliases of *"append"*)

Each time you trigger an event, it is stored in *Handler.events*. You can empty past events by calling *"clear_events"* or all (events and callbacks) with *"clear"*.

.. literalinclude:: ../../tests/examples/subject_observer.py
   :caption: tests/examples/subject_observer.py
   :name: subject_observer


-----------------------------
Observe a method
-----------------------------
To observe a method, you can:
  - declare your method at class level with *"Method"* and a function as first argument
  - decorate a method with *"Method"*
  - use functions *"handle"*, *"before"* or *"after"* on class or object callable attribute with type of event in the optionalthird argument (recommended)

Method events objects are of type BeforeEvent and AfterEvent y default.

They have 4 main attributes:
  - *"subject"*: the object instance where event happens
  - *"name"*: the method name of the object instance
  - *"args"*: the tuple of passed args
  - *"kwargs"*: the dict of named args


.. literalinclude:: ../../tests/examples/method.py
   :caption: tests/examples/method.py
   :name: method


---------------------------------
Observe an attribute
---------------------------------
*"Attribute"* is like *"Method"*, to observe it you can:
  - declare your attribute at class level with *"Attribute"* and an optionnal default value as first argument
  - decorate an existing attribute with *"Attribute"*
  - use functions *"handle"*, *"on_get"*, *"on_change"*, *"on_set"*, *"on_del"* on class or object attribute with the type of event on the third argument (recommended)


Attribute events objects are of type OnGetEvent, OnChangeEvent, OnSetEvent, OnDelEvent.

They have 3 main attributes:
  - *"subject"*: the object instance where event happens
  - *"name"*: the attribute name of the object instance
  - *"value"*: the attribute value if set

In addition each kwarg is added to event as an attribute. (like "content" in ex 0)


.. literalinclude:: ../../tests/examples/attribute.py
   :caption: tests/examples/attribute.py
   :name: attribute

