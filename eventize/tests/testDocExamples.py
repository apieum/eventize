# -*- coding: utf8 -*-
from . import TestCase
from eventize import EventedMethod, EventedAttribute

class DocExamplesTest(TestCase):

    def test_example_1_EventedMethod(self):

        class Observed(object):
            def __init__(self):
                self.valid = False
                self.logs=[]

            @EventedMethod
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
        my_object.is_valid.before += my_logs.log_before
        my_object.is_valid.before.called_with('permute').do(my_object.not_valid)
        my_object.is_valid.after += my_logs.log_after

        assert my_object.is_valid() is False
        assert my_object.is_valid('permute') is True

        assert my_logs == [
            my_logs.message('before', is_valid=False),
            my_logs.message('after', is_valid=False),
            my_logs.message('before', 'permute', is_valid=False),
            my_logs.message('after', 'permute', is_valid=True),
        ]

    def test_example_2_EventedAttribute(self):
        class Validator(object):
            def __init__(self, is_valid=False):
                self.valid = is_valid

        class Observed(object):
            validator = EventedAttribute(default=Validator(False))

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


    def test_example_2_1_EventedAttribute(self):
        class Observed(object):
            valid = EventedAttribute(False)

        class Logger(list):
            def log_set(self, event):
                self.append(self.message('on_set', event.name, event.value))

            def log_set_error(self, event):
                self.append(self.message('on_set_error', event.name, event.value))

            def message(self, event_name, attr_name, value):
                return "'%s' called for attribute '%s', with value '%s'" % (event_name, attr_name, value)

        my_object = Observed()
        other_object = Observed()
        dont_change_value = lambda event: setattr(event, 'value', event.subject.valid)
        my_logs = Logger()
        getting_my_object = Observed.valid.on_set.called_with(subject=my_object)
        getting_my_object += my_logs.log_set
        getting_my_object.called_with_type(value=type(None)).do(my_logs.log_set_error).then(dont_change_value)

        my_object.valid = True
        my_object.valid = None
        other_object.valid = True
        other_object.valid = None

        assert my_object.valid == True

        assert my_logs == [
            my_logs.message('on_set', 'valid', True),
            my_logs.message('on_set', 'valid', None),
            my_logs.message('on_set_error', 'valid', None),
        ]



