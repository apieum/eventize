from .. import TestCase, Mock
from eventize import Attribute, handle, on_get, on_set
from eventize.method import BeforeDescriptor, BeforeEvent
from eventize.events import Expect


class ClassWithAttr(object):
    attribute = None

class ExpectTest(TestCase):
    def setUp(self):
        self.obj = ClassWithAttr()
        handle(self.obj, 'attribute').clear_all()

    def test_can_observe_get_event_for_given_instances(self):
        event = Mock()
        obj1 = ClassWithAttr()
        obj1.attribute = "value"
        obj2 = ClassWithAttr()
        obj2.attribute = "value"
        obj3 = ClassWithAttr()
        obj3.attribute = "value"

        is_obj1_or_obj3 = Expect.subject(obj1) | Expect.subject(obj3)
        on_get(ClassWithAttr, 'attribute').when(is_obj1_or_obj3).do(event)

        getattr(obj1, 'attribute', None)
        getattr(obj2, 'attribute', None)
        getattr(obj3, 'attribute', None)

        self.assertEqual(2, event.call_count)

    def test_can_observe_set_event_for_given_values(self):
        event = Mock()
        expect_value = Expect.value('foo') | Expect.value('bar')

        set_attr = on_set(ClassWithAttr, 'attribute')
        set_attr.when(expect_value).do(event)

        self.obj.attribute = "foo"
        self.obj.attribute = "value"
        self.obj.attribute = "bar"
        self.assertEqual(2, event.call_count)

    def test_can_observe_events_within_kwarg_instance_type(self):
        event = Mock()
        value_is_boolean = Expect.value.instance_of(bool)

        set_attr = on_set(ClassWithAttr, 'attribute')
        set_attr.when(value_is_boolean).do(event)
        obj = ClassWithAttr()
        obj.attribute = False

        event.assert_called_once_with(set_attr.events[0])

    def test_can_observe_events_within_kwarg_type(self):
        event = Mock()
        value_type_is_object = Expect.value.type_is(object)

        set_attr = on_set(ClassWithAttr, 'attribute')
        set_attr.when(value_type_is_object).do(event)
        obj = ClassWithAttr()
        obj.attribute = list([1, 2, 3])
        obj.attribute = object()

        event.assert_called_once_with(set_attr.events[1])

    def test_can_use_when_on_handle(self):
        event = Mock()
        expected = "value"
        value_is_expected = Expect.value(expected)

        set_attr = handle(self.obj, 'attribute')
        set_attr.when(value_is_expected).on_set_class += event

        self.obj.attribute = expected
        self.obj.attribute = ""
        event.assert_called_once_with(set_attr.on_set.events[0])


    def test_can_add_condition_about_args(self):
        func = Mock()
        self.instance = BeforeDescriptor()
        self.name = "expect"
        event1 = BeforeEvent(self, valid=True)
        event2 = BeforeEvent(self, valid=False)
        self.instance.when(Expect.kwargs(valid=True)).do(func)
        self.instance(event1)
        self.instance(event2)
        func.assert_called_once_with(event1)
        del self.instance
        del self.name
