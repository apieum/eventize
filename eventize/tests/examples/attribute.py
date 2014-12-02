from eventize import handle, on_get, Attribute
from eventize.attribute import OnGetEvent, OnGetHandler


class Validator(object):
    def __init__(self, is_valid):
        self.valid = is_valid
    def __call__(self):
        return self.valid

class Observed(object):
    validate = Validator(False)

class Logger(list):
    def log_get(self, event):
        assert type(event) is OnGetEvent, "Get event of type %s" % type(event)
        self.append(self.message('on_get', event.name, event.value()))
    def log_change(self, event):
        self.append(self.message('on_change', event.name, event.value()))
    def log_set(self, event):
        self.append(self.message('on_set', event.name, event.value()))
    def log_del(self, event):
        self.append(self.message('on_del', event.name, event.value()))

    def message(self, event_name, attr_name, value):
        return "'%s' called for attribute '%s', with value '%s'" % (event_name, attr_name, value)

my_object = Observed()
my_logs = Logger()
my_object_validate = handle(my_object, 'validate')
my_object_validate.on_get += my_logs.log_get
my_object_validate.on_change += my_logs.log_change
my_object_validate.on_set += my_logs.log_set
my_object_validate.on_del += my_logs.log_del

Observed_validate = handle(Observed, 'validate')
Observed_validate.on_get += my_logs.log_get
Observed_validate.on_change += my_logs.log_change
Observed_validate.on_set += my_logs.log_set
Observed_validate.on_del += my_logs.log_del

# same result with my_object.validate
is_valid = getattr(my_object, 'validate')
# check if default value is False as defined in class
assert is_valid() == False, '[error] Default value was not set'
# same result with my_object.validate = Validator(True)
setattr(my_object, 'validate', Validator(True))
# same result with del my_object.validate
delattr(my_object, 'validate')

assert my_logs == [
    my_logs.message('on_get', 'validate', False),  # Called at class level
    my_logs.message('on_get', 'validate', False),  # Called at instance level
    my_logs.message('on_set', 'validate', True),   # Called at class level
    my_logs.message('on_set', 'validate', True),   # Called at instance level
    my_logs.message('on_change', 'validate', True),   # Called at class level
    my_logs.message('on_change', 'validate', True),   # Called at instance level
    my_logs.message('on_del', 'validate', True),   # Called at class level
    my_logs.message('on_del', 'validate', True),   # Called at instance level
]

# You can use your own events types
class OnGetCall(OnGetEvent):
    def returns(self):
        return self.value()

# and override Attribute or Method types
class CallAttr(Attribute):
    # must be redefined otherwise callbacks are appended to class Attribute
    # see advanced usage -> inheritance
    on_get = OnGetHandler()


my_object = Observed()
# third argument permits to set new type of attribute
on_get_validate = on_get(my_object, 'validate', CallAttr)
# set event type
on_get_validate.event_type = OnGetCall

assert isinstance(Observed.validate, CallAttr)

# OnGetCall Event returns my_object.validate()
assert my_object.validate is False
assert len(on_get_validate) == 0, "Expect my_object.validate.on_get has no callbacks"


def set_to_true(event):
    assert type(event) == OnGetCall
    event.value = Validator(True)

# All objects with CallAttr attribute will call set_to_true
CallAttr.on_get += set_to_true

# set_to_true change value and check event is of type OnGetCall
assert my_object.validate is True

# remove all callbacks and events at descriptor, class and instance level
handle(my_object, 'validate').clear_all()

assert len(CallAttr.on_get) == 0
