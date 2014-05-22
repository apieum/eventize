from .. import TestCase, Mock
from eventize import Observable, Method, Attribute


class ApiDecoratorsTest(TestCase):
    def test_it_can_make_all_object_methods_observable(self):
        @Observable
        class Observed(object):
            def method(self):
                return True

        observed = Observed()
        self.assertTrue(observed.method())
        self.assertIsInstance(Observed.method, Method)

    def test_it_can_make_all_object_attributes_observable(self):
        expected = 10
        @Observable
        class Observed(object):
            attribute = expected

        observed = Observed()
        self.assertEqual(observed.attribute, expected)
        self.assertIsInstance(Observed.attribute, Attribute)

    def test_it_can_make_methods_observable(self):
        class Observed(object):
            @Method
            def method(self):
                return True

        observed = Observed()
        self.assertTrue(observed.method())
        self.assertIsInstance(Observed.method, Method)

    def test_it_can_make_attributes_observable(self):
        expected = "20"
        class Observed(object):
            attribute = Attribute(expected)

        observed = Observed()
        self.assertEqual(observed.attribute, expected)
        self.assertIsInstance(Observed.attribute, Attribute)

    def test_Method_can_be_set_at_class_level(self):
        self_valid = lambda self: self.valid

        class Observed(object):
            valid = False
            is_valid = Method(self_valid)

        observed = Observed()
        self.assertFalse(observed.is_valid())
        observed.valid = True
        self.assertTrue(observed.is_valid())
        self.assertIsInstance(Observed.is_valid, Method)

