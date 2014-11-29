=============
Introduction
=============


Eventize permits to listen to *"before"* and *"after"* methods events and *"on_get"*, *"on_change"*, *"on_set"*, *"on_del"* attributes events.

**Features:**
  * Can be used as a simple subject/observer pattern
  * Conditional events
  * Use descriptors to lazily and unobstrusively listen to "on_get", "on_change","on_set", "on_del" events on attributes and "before" and "after" events on methods.
  * Precise callbacks inheritance (see Subject)
  * Statically and dynamically customizable (via inheritance, pattern visitor over a "*modifier*" protocol, decorators...)

**Fine grained event dispatcher**

It can listen to events at 3 levels (by order of execution):
  * **Descriptor Class**: for all classes which use the given Attribute or Method descriptor class
  * **Descriptor Instance**: for all objects of a given class
  * **Object instance**: for the given object attribute value or method

