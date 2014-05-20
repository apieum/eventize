# -*- coding: utf8 -*-
from .. import TestCase, Mock
from eventize.api import Method, Attribute, handle, on_get, on_set, on_del, before, after

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
        self.assertIs(given, Observed.attribute.on_set_instance(observed))

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
