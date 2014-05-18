# -*- coding: utf8 -*-
from . import TestCase, Mock
from eventize import Observable, ObservedMethod, ObservedAttribute
from eventize import handle, on_get, on_set, on_del, before, after


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
    def test_handle_makes_and_returns_observed_method_from_class(self):
        class Observed(object):
            def method(self):
                return True
        given = handle(Observed, "method")
        self.assertIs(given, Observed.method)
        self.assertIsInstance(Observed.method, ObservedMethod)

    def test_handle_makes_and_returns_observed_method_from_object(self):
        class Observed(object):
            def method(self):
                return True
        observed = Observed()
        given = handle(observed, "method")
        self.assertIsInstance(Observed.method, ObservedMethod)

    def test_handle_makes_and_returns_observed_method_once(self):
        class Observed(object):
            def method(self):
                return True
        given = handle(Observed, "method")
        expected = handle(Observed, "method")
        self.assertIs(given, expected)

    def test_handle_makes_and_returns_observed_attribute_from_class(self):
        class Observed(object):
            attribute = "attr"

        given = handle(Observed, "attribute")
        self.assertIs(given, Observed.attribute)
        self.assertIsInstance(Observed.attribute, ObservedAttribute)

    def test_on_get_returns_observed_attribute_on_get(self):
        class Observed(object):
            attribute = "attr"

        given = on_get(Observed, "attribute")
        self.assertIs(given, Observed.attribute.on_get)

    def test_on_set_returns_observed_attribute_on_set(self):
        class Observed(object):
            attribute = "attr"

        observed = Observed()
        given = on_set(observed, "attribute")
        self.assertIs(given, observed.attribute.on_set)

    def test_on_del_returns_observed_attribute_on_del(self):
        class Observed(object):
            attribute = "attr"

        given = on_del(Observed, "attribute")
        self.assertIs(given, Observed.attribute.on_del)

    def test_before_returns_observed_method_before(self):
        class Observed(object):
            def method(self):
                return

        given = before(Observed, "method")
        self.assertIs(given, Observed.method.before)

    def test_after_returns_observed_method_after(self):
        class Observed(object):
            def method(self):
                return

        given = after(Observed, "method")
        self.assertIs(given, Observed.method.after)

