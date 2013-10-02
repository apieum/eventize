# -*- coding: utf8 -*-
import unittest
from mock import Mock
from eventize.method import Method
from eventize.eventize import Observable, ObservedMethod


class EventizeTest(unittest.TestCase):
    def test_it_can_make_all_object_methods_observable(self):
        @Observable
        class Observed(object):
            def method(self):
                return True

        observed = Observed()
        self.assertTrue(observed.method())
        self.assertIsInstance(Observed.method, Method)
        observed.method.on += Mock()
        self.assertTrue(hasattr(Observed.method, 'on'))
        self.assertTrue(hasattr(observed.method, 'on'))

    def test_it_can_make_methods_observable(self):
        class Observed(object):
            @ObservedMethod
            def method(self):
                return True

        observed = Observed()
        self.assertTrue(observed.method())
        self.assertIsInstance(Observed.method, Method)
        Observed.method.before += Mock()
        self.assertTrue(hasattr(Observed.method, 'before'))
        self.assertTrue(hasattr(observed.method, 'before'))
