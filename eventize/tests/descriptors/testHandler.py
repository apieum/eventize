# -*- coding: utf8 -*-
from .. import TestCase, Mock
from eventize.descriptors import Handler, WrapCondition
from eventize.events import Expect

class Wrapped(object):
    handler1 = Handler()
    handler2 = Handler()


class WrapConditionTest(TestCase):
    def setUp(self):
        Wrapped.handler1.remove_all()

    def test_it_has_given_properties(self):
        given = {'handler1': Wrapped.handler1, }
        wrapper = WrapCondition(given, lambda *args: True)
        self.assertTrue(hasattr(wrapper, 'handler1'))
        self.assertFalse(hasattr(wrapper, 'handler2'))

    def test_its_properties_returns_handler_when_condition(self):
        handlers = {'handler1': Wrapped.handler1, }
        condition = lambda *args: True
        wrapper = WrapCondition(handlers, condition)
        expected = Wrapped.handler1.when(condition)
        self.assertEqual(wrapper.handler1, expected)

    def test_it_wrap_object_to(self):
        desc = Wrapped()
        handlers = {'handler1': desc.handler1, }
        condition = lambda *args: False
        wrapper = WrapCondition(handlers, condition)
        expected = desc.handler1.when(condition)
        self.assertEqual(wrapper.handler1, expected)
        self.assertEqual(0, len(Wrapped.handler1))
