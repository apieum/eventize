# -*- coding: utf8 -*-
from . import TestCase

class DocExamplesTest(TestCase):

    def test_example_0_as_a_simple_subject_observer_pattern(self):
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
        assert handler.events == (event1, event2)
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


    def test_example_1_ObservedMethod(self):

        from eventize import before, after
        from eventize.method import BeforeEvent, AfterEvent
        from eventize.events import Expect

        class Observed(object):
            def __init__(self):
                self.valid = False

            def is_valid(self, *args):
                return self.valid

            def not_valid(self, event):
                assert event.name == "is_valid" # (event subject name)
                assert event.subject == self
                self.valid = not self.valid

        class Logger(list):
            def log_before(self, event):
                assert type(event) is BeforeEvent
                self.append(self.message('before %s'  % event.name, *event.args, is_valid=event.subject.valid))

            def log_after(self, event):
                assert type(event) is AfterEvent
                self.append(self.message('after %s' % event.name, *event.args, is_valid=event.subject.valid))

            def message(self, event_name, *args, **kwargs):
                return "%s called with args: '%s', current:'%s'" % (event_name, args, kwargs['is_valid'])



        my_object = Observed()
        my_logs = Logger()
        args_have_permute = Expect.arg('permute')

        before_is_valid = before(my_object, 'is_valid')
        before_is_valid += my_logs.log_before
        before_is_valid.when(args_have_permute).do(my_object.not_valid)
        after(my_object, 'is_valid').do(my_logs.log_after)

        assert my_object.is_valid() is False
        assert my_object.is_valid('permute') is True

        assert my_logs == [
            my_logs.message('before is_valid', is_valid=False),
            my_logs.message('after is_valid', is_valid=False),
            my_logs.message('before is_valid', 'permute', is_valid=False),
            my_logs.message('after is_valid', 'permute', is_valid=True),
        ]

    def test_example_2_Observe_an_Attribute(self):

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
            # see example 3 for callbacks inheritance
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
        self.assertEqual(my_object.validate, True)

        # remove all callbacks and events at descriptor, class and instance level
        handle(my_object, 'validate').clear_all()

        assert len(CallAttr.on_get) == 0


    def test_example_3_inheritance(self):

        from eventize import Attribute
        from eventize.attribute import Subject, OnSetHandler

        def validate_string(event):
            if isinstance(event.value, type('')): return

            message = "%s.%s must be a string!" % (type(event.subject).__name__, event.name)
            raise TypeError(message)

        def titlecase(event):
            event.value = event.value.title()

        class StringAttribute(Attribute):
            on_set = OnSetHandler(validate_string)

        # Subject == events.Subject(OnGetHandler, OnSetHandler, OnChangeDescriptor, OnDelDescriptor)
        @Subject  # Attach StringAttribute.on_set callbacks to Name.on_set
        class Name(StringAttribute):
            on_set = OnSetHandler(titlecase)

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

