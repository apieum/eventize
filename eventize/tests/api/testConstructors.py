# -*- coding: utf8 -*-
from .. import TestCase, Mock
from eventize import handle, on_get, on_set, on_del, on_change, before, after
from eventize import Method, Attribute


class ApiConstructorsTest(TestCase):
    def test_handle_makes_and_returns_observed_method_from_class(self):
        class Observed(object):
            def method(self):
                return True
        given = handle(Observed, "method")
        self.assertIs(given, Observed.method)
        self.assertIsInstance(Observed.method, Method)

    def test_handle_makes_and_returns_observed_method_from_object(self):
        class Observed(object):
            def method(self):
                return True
        observed = Observed()
        given = handle(observed, "method")
        self.assertIsInstance(Observed.method, Method)

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
        self.assertIsInstance(Observed.attribute, Attribute)

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
        self.assertIs(given, Observed.attribute.get_value(observed).on_set)

    def test_on_del_returns_observed_attribute_on_del(self):
        class Observed(object):
            attribute = "attr"

        given = on_del(Observed, "attribute")
        self.assertIs(given, Observed.attribute.on_del)

    def test_on_change_returns_observed_attribute_on_change(self):
        class Observed(object):
            attribute = "attr"

        given = on_change(Observed, "attribute")
        self.assertIs(given, Observed.attribute.on_change)

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

    def test_can_inject_handler_type_in_handle(self):
        class Observed(object):
            attribute = "attr"

        class MyAttr(Attribute):
            pass
        given = handle(Observed, "attribute", MyAttr)
        self.assertIsInstance(Observed.attribute, MyAttr)

    def test_can_inject_handler_type_in_handler_with_event(self):
        class Observed(object):
            def method(self):
                return

        class MyMethod(Method):
            pass
        given = before(Observed, "method", MyMethod)
        self.assertIsInstance(Observed.method, MyMethod)

    def test_when_handler_already_defined_dont_set_it_again(self):
        class Observed(object):
            attribute = False

        expected = on_get(Observed, "attribute")
        self.assertIs(expected, on_get(Observed, "attribute"))
        obj = Observed()
        expected = on_get(obj, "attribute")
        self.assertIs(expected, on_get(obj, "attribute"))

    def test_can_override_handler_type_if_set(self):
        class Observed(object):
            def method(self):
                return

        class MyMethod(Method):
            pass

        handle(Observed, 'method')
        given = before(Observed, "method", MyMethod)
        self.assertIsInstance(Observed.method, MyMethod)

    def test_when_overriding_handler_default_is_correctly_set(self):
        expected = 'expected'
        class Observed(object):
            attribute = Attribute(expected)

        class OtherAttr(Attribute):
            pass

        ClsAttr = handle(Observed, "attribute", OtherAttr)
        ObjAttr = handle(Observed(), "attribute", OtherAttr)

        self.assertEqual(expected, ClsAttr.default)
        self.assertEqual(expected, ObjAttr.get())
