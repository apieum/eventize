# -*- coding: utf8 -*-
from . import TestCase

class DocExamplesTest(TestCase):

    def test_example_1_ObservedMethod(self):

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

    def test_example_2_ObservedAttribute(self):

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


    def test_example_3_ObservedAttribute(self):
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


    def test_example_4_inheritance(self):
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

    def test_example_5_choose_your_handler(self):
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



