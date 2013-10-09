# -*- coding: utf8 -*-
from mock import Mock
from eventize.events.conditional import Conditional
from eventize.events.event import Event

from liskov import subtype, append_sys_path
append_sys_path(__file__)

class ConditionalHandlerTest(subtype('testHandler.EventHandlerTest')):

    def test_conditional_take_an_extra_argument_named_condition(self):
        func = lambda: True
        handler = self.new_handler(condition=func)
        self.assertIs(func, handler.condition)

    def test_condition_must_be_callable(self):
        expected = "not callable"
        with self.assertRaisesRegex(TypeError, expected):
            self.new_handler(condition=expected)

    def test_event_is_not_propagated_if_condition_is_false(self):
        condition = lambda event: False
        event = Event(self)
        func = Mock()
        handler = self.new_handler(func, condition=condition)
        handler(event)

        self.assertIs(0, func.call_count)


    def new_handler(self, *args, **kwargs):
        return Conditional(*args, **kwargs)
