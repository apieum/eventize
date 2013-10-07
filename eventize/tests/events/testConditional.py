# -*- coding: utf8 -*-
from mock import Mock
from eventize.events.conditional import Conditional
from eventize.events.event import Event

from liskov import subtype, append_sys_path
append_sys_path(__file__)

class ConditionalSlotTest(subtype('testSlot.EventSlotTest')):

    def test_conditional_take_an_extra_argument_named_condition(self):
        func = lambda: True
        slot = self.new_slot(condition=func)
        self.assertIs(func, slot.condition)

    def test_condition_must_be_callable(self):
        expected = "not callable"
        with self.assertRaisesRegex(TypeError, expected):
            self.new_slot(condition=expected)

    def test_event_is_not_propagated_if_condition_is_false(self):
        condition = lambda event: False
        event = Event(self)
        func = Mock()
        slot = self.new_slot(func, condition=condition)
        slot(event)

        self.assertIs(0, func.call_count)


    def new_slot(self, *args, **kwargs):
        return Conditional(*args, **kwargs)
