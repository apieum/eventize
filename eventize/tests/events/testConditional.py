# -*- coding: utf8 -*-
from mock import Mock
from eventize.events.conditional import Conditional

class TestLiskovSubstitution(type):
    def __new__(cls, name, bases, attrs):
        from testSlot import EventSlotTest
        bases = (EventSlotTest, ) + bases
        return type.__new__(cls, name, bases, attrs)


class ConditionalSlotTest(object):
    __metaclass__ = TestLiskovSubstitution

    def test_conditional_take_an_extra_argument_named_condition(self):
        func = lambda: True
        slot = self.new_slot(condition=func)
        self.assertIs(func, slot.condition)

    def test_condition_must_be_callable(self):
        expected = "not callable"
        with self.assertRaisesRegexp(TypeError, expected):
            self.new_slot(condition=expected)

    def test_event_is_not_propagated_if_condition_is_false(self):
        condition = lambda: False
        func = Mock()
        slot = self.new_slot(func, condition=condition)
        slot()

        self.assertIs(0, func.call_count)

    def test_conditional_do_method_is_same_as_append(self):
        func = Mock()
        slot = self.new_slot()
        slot.do(func)

        self.assertIs(func, slot[0])


    def new_slot(self, *args, **kwargs):
        return Conditional(*args, **kwargs)
