# -*- coding: utf8 -*-
from . import TestCase, Mock
from eventize import Observable, ObservedMethod, ObservedAttribute
from eventize import handle


class EventizeDecoratorsTest(TestCase):
    def test_it_can_make_all_object_methods_observable(self):
        @Observable
        class Observed(object):
            def method(self):
                return True

        observed = Observed()
        self.assertTrue(observed.method())
        self.assertIsInstance(Observed.method, ObservedMethod)
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
        self.assertIsInstance(Observed.attribute, ObservedAttribute)
        self.assertTrue(hasattr(Observed.attribute, 'on_get'))
        self.assertTrue(hasattr(observed.attribute, 'on_get'))

    def test_it_can_make_methods_observable(self):
        class Observed(object):
            @ObservedMethod
            def method(self):
                return True

        observed = Observed()
        self.assertTrue(observed.method())
        self.assertIsInstance(Observed.method, ObservedMethod)
        Observed.method.before += Mock()
        self.assertTrue(hasattr(Observed.method, 'before'))
        self.assertTrue(hasattr(observed.method, 'before'))

    def test_it_can_make_attributes_observable(self):
        expected = "20"
        class Observed(object):
            attribute = ObservedAttribute(expected)

        observed = Observed()
        self.assertEqual(observed.attribute, expected)
        self.assertIsInstance(Observed.attribute, ObservedAttribute)
        self.assertTrue(hasattr(Observed.attribute, 'on_set'))
        self.assertTrue(hasattr(observed.attribute, 'on_set'))

    def test_ObservedMethod_can_be_set_at_class_level(self):
        self_valid = lambda self: self.valid

        class Observed(object):
            valid = False
            is_valid = ObservedMethod(self_valid)

        observed = Observed()
        self.assertFalse(observed.is_valid())
        observed.valid = True
        self.assertTrue(observed.is_valid())
        self.assertIsInstance(Observed.is_valid, ObservedMethod)


class EventizeHandlersTest(TestCase):
    def test_handle_makes_observed_method_from_class(self):
        class Observed(object):
            def method(self):
                return True
        handle(Observed, "method")
        self.assertIsInstance(Observed.method, ObservedMethod)

    def test_handle_returns_observed_method(self):
        class Observed(object):
            def method(self):
                return True
        given = handle(Observed, "method")
        self.assertIs(given, Observed.method)

    def test_handle_makes_observed_method_from_object(self):
        class Observed(object):
            def method(self):
                return True
        observed = Observed()
        given = handle(observed, "method")
        self.assertIsInstance(Observed.method, ObservedMethod)

    def test_handle_makes_observed_method_once(self):
        class Observed(object):
            def method(self):
                return True
        given = handle(Observed, "method")
        expected = handle(Observed, "method")
        self.assertIs(given, expected)
