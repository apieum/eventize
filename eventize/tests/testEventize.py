# -*- coding: utf8 -*-
from . import TestCase, Mock
from eventize import Observable, EventedMethod, EventedAttribute


class EventizeTest(TestCase):
    def test_it_can_make_all_object_methods_observable(self):
        @Observable
        class Observed(object):
            def method(self):
                return True

        observed = Observed()
        self.assertTrue(observed.method())
        self.assertIsInstance(Observed.method, EventedMethod)
        observed.method.before += Mock()
        self.assertTrue(hasattr(Observed.method, 'before'))
        self.assertTrue(hasattr(observed.method, 'before'))

    def test_it_can_make_all_object_attributes_observable(self):
        expected = 10
        @Observable
        class Observed(object):
            attribute = expected

        observed = Observed()
        self.assertEqual(observed.attribute, expected)
        self.assertIsInstance(Observed.attribute, EventedAttribute)
        self.assertTrue(hasattr(Observed.attribute, 'on_get'))
        self.assertTrue(hasattr(observed.attribute, 'on_get'))

    def test_it_can_make_methods_observable(self):
        class Observed(object):
            @EventedMethod
            def method(self):
                return True

        observed = Observed()
        self.assertTrue(observed.method())
        self.assertIsInstance(Observed.method, EventedMethod)
        Observed.method.before += Mock()
        self.assertTrue(hasattr(Observed.method, 'before'))
        self.assertTrue(hasattr(observed.method, 'before'))

    def test_it_can_make_attributes_observable(self):
        expected = "20"
        class Observed(object):
            attribute = EventedAttribute(expected)

        observed = Observed()
        self.assertEqual(observed.attribute, expected)
        self.assertIsInstance(Observed.attribute, EventedAttribute)
        self.assertTrue(hasattr(Observed.attribute, 'on_set'))
        self.assertTrue(hasattr(observed.attribute, 'on_set'))

    def test_EventedMethod_can_be_set_at_class_level(self):
        self_valid = lambda self: self.valid

        class Observed(object):
            valid = False
            is_valid = EventedMethod(self_valid)

        observed = Observed()
        self.assertFalse(observed.is_valid())
        observed.valid = True
        self.assertTrue(observed.is_valid())
        self.assertIsInstance(Observed.is_valid, EventedMethod)
