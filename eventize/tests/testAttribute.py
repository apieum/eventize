# -*- coding: utf8 -*-
import unittest
from mock import Mock
from eventize.attribute import Attribute

class ClassWithAttribute(object):
    attribute = Attribute()

class AttributeTest(unittest.TestCase):
    def test_setting_Attribute_store_value_in_instance_dict(self):
        obj = ClassWithAttribute()
        obj.attribute = 'value'

        self.assertEqual('value', obj.__dict__['attribute'])
        self.assertIsInstance(obj.__class__.attribute, Attribute)

    def test_can_delete_attribute(self):
        obj = ClassWithAttribute()
        obj.attribute = 'value'
        del obj.attribute

        self.assertNotIn('attribute', obj.__dict__)

    def test_if_attribute_not_set_expect_AttributeError(self):
        expectedMsg = "AttributeError: 'ClassWithAttribute' object has no attribute 'attribute'"
        obj = ClassWithAttribute()
        with self.assertRaises(AttributeError) as context:
            obj.attribute
        self.assertEqual(context.exception.message, expectedMsg)

    def test_not_set_attribute_returns_default_if_set(self):
        expected = 'default'
        class test(object):
            attribute = Attribute(expected)

        obj = test()

        self.assertEqual(obj.attribute, expected)

    def test_can_observe_get_event(self):
        on_get = Mock()
        ClassWithAttribute.attribute.on_get += on_get
        obj = ClassWithAttribute()

        getattr(obj, 'attribute', None)

        on_get.assert_called_once_with(obj, 'attribute')

    def test_can_observe_set_event(self):
        on_set = Mock()
        ClassWithAttribute.attribute.on_set += on_set
        obj = ClassWithAttribute()
        value = "value"

        setattr(obj, 'attribute', value)

        on_set.assert_called_once_with(obj, 'attribute', value)

    def test_can_observe_del_event(self):
        on_del = Mock()
        ClassWithAttribute.attribute.on_del += on_del
        obj = ClassWithAttribute()

        del obj.attribute

        on_del.assert_called_once_with(obj, 'attribute')


    def test_can_observe_get_event_for_a_given_instance(self):
        on_get = Mock()
        obj1 = ClassWithAttribute()
        obj2 = ClassWithAttribute()
        obj3 = ClassWithAttribute()

        ClassWithAttribute.attribute.on_get.called_with(obj1).do(on_get)
        ClassWithAttribute.attribute.on_get.called_with(obj3).do(on_get)

        getattr(obj1, 'attribute', None)
        getattr(obj2, 'attribute', None)
        getattr(obj3, 'attribute', None)

        self.assertEqual(2, on_get.call_count)

    def test_can_observe_set_event_for_a_given_instance(self):
        on_set = Mock()
        obj = ClassWithAttribute()
        value = "value"

        ClassWithAttribute.attribute.on_set.called_with(obj).do(on_set)

        obj.attribute = value
        on_set.assert_called_once_with(obj, 'attribute', value)


    def test_can_observe_set_event_for_a_given_value(self):
        on_set = Mock()
        obj = ClassWithAttribute()
        value = "value"

        ClassWithAttribute.attribute.on_set.called_with(value).do(on_set)

        obj.attribute = "foo"
        obj.attribute = value
        obj.attribute = "bar"
        self.assertEqual(1, on_set.call_count)

    def test_can_observe_del_event_for_a_given_instance(self):
        on_del = Mock()
        obj = ClassWithAttribute()

        ClassWithAttribute.attribute.on_del.called_with(obj).do(on_del)

        delattr(obj, 'attribute')
        on_del.assert_called_once_with(obj, 'attribute')

    def test_it_add_events_attributes_to_instance_value(self):
        obj = ClassWithAttribute()
        obj.attribute = "value"

        att_items = dir(obj.attribute)

        self.assertIn('on_get', att_items)
        self.assertIn('on_set', att_items)
        self.assertIn('on_del', att_items)

    def test_on_get_value_event_is_triggered_only_for_given_instance(self):
        on_get = Mock()
        obj1 = ClassWithAttribute()
        obj2 = ClassWithAttribute()
        obj1.attribute = "value"
        obj2.attribute = "value"

        obj1.attribute.on_get += on_get
        obj2.attribute.on_get += on_get

        getattr(obj1, 'attribute')

        self.assertEqual(1, on_get.call_count)

    def test_on_set_and_on_del_value_events_are_triggered_only_for_given_instance(self):
        on_set = Mock()
        on_del = Mock()
        obj1 = ClassWithAttribute()
        obj2 = ClassWithAttribute()
        obj1.attribute = 10
        obj2.attribute = [1, 2, 3]

        obj1.attribute.on_set.do(on_set)
        obj2.attribute.on_set.do(on_set)
        obj1.attribute.on_del.do(on_del)
        obj2.attribute.on_del.do(on_del)

        obj1.attribute = {'value': obj1.attribute}
        del obj2.attribute

        self.assertEqual(1, on_set.call_count)
        self.assertEqual(1, on_del.call_count)

    def test_value_events_preserve_object_class_and_contents(self):
        class MyClass(object):
            attr = 10

        obj1 = ClassWithAttribute()
        obj2 = MyClass()
        obj2.attr = 20

        obj1.attribute = obj2

        self.assertEqual(20, obj1.attribute.attr)
        self.assertEqual(MyClass, obj1.attribute.__class__)



    def test_value_events_preserve_types(self):
        obj = ClassWithAttribute()
        obj.attribute = 30

        self.assertIsInstance(obj.attribute, type(30))
