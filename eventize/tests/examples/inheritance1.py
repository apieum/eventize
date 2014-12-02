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
@Subject
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
