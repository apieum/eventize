# -*- coding: utf8 -*-
from .. import TestCase, Mock
from eventize.events import Handler, Event


class EventHandlerTest(TestCase):
    def test_a_Handler_is_callable(self):
        handler = self.new_handler()
        self.assertTrue(callable(handler))

    def test_a_Handler_is_a_list_of_callable(self):
        handler = self.new_handler()
        handler.append(self.new_callback())
        handler.append(self.new_callback())
        self.assertEqual(len(handler), 2)

    def test_do_method_is_same_as_append(self):
        handler = self.new_handler()
        self.assertEqual(handler.append, handler.do)

    def test_then_method_is_same_as_append(self):
        handler = self.new_handler()
        self.assertEqual(handler.append, handler.then)

    def test_an_Handler_raise_an_error_when_appending_a_non_callable_item(self):
        handler = self.new_handler()
        with self.assertRaisesRegex(TypeError, 'string'):
            handler.append('string')

    def test_an_Handler_raise_an_error_when_setting_a_non_callable_item(self):
        handler = self.new_handler()
        handler.append(self.new_callback())
        with self.assertRaisesRegex(TypeError, 'string'):
            handler[0] = 'string'

    def test_when_an_handler_is_called_all_its_contents_is_called(self):
        mock1 = self.new_callback()
        mock2 = self.new_callback()
        handler = self.new_handler()
        handler.append(mock1)
        handler.append(mock2)
        event = Event(self)
        handler(event)

        self.assertEqual(1, mock1.call_count)
        self.assertEqual(1, mock2.call_count)

    def test_when_an_observer_raises_StopPropagation_following_observers_are_not_executed(self):
        def func1(event):
            event.stop_propagation()

        mock = self.new_callback()
        handler = self.new_handler()
        handler.append(func1)
        handler.append(mock)
        handler(Event(self))

        self.assertEqual(0, mock.call_count)

    def test_Handler_arguments_is_the_list_content(self):
        expected1 = self.new_callback()
        expected2 = self.new_callback()
        handler = self.new_handler(expected1, expected2)

        self.assertIs(handler[0], expected1)
        self.assertIs(handler[1], expected2)

    def test_cannot_append_non_callable_by_handler_arguments(self):
        expected_exception = 'invalid value 10'
        with self.assertRaisesRegex(TypeError, expected_exception):
            self.new_handler(expected_exception)

    def test_cannot_append_non_callable_by_handler_extend(self):
        expected_exception = 'invalid value 20'
        handler = self.new_handler()
        with self.assertRaisesRegex(TypeError, expected_exception):
            handler.extend([expected_exception])

    def test_cannot_append_non_callable_by_handler_insert(self):
        expected_exception = 'invalid value 30'
        handler = self.new_handler(self.new_callback(), self.new_callback())
        with self.assertRaisesRegex(TypeError, expected_exception):
            handler.insert(0, expected_exception)

    def test_when_propagation_is_stopped_event_contains_message(self):
        expected = 'message'
        def func(event):
            event.stop_propagation(expected)

        handler = self.new_handler(func)
        event = Event(self)
        handler(event)

        self.assertEqual(event.messages[0], expected)

    def test_can_append_observer_with_iadd_symbol(self):
        func = lambda: True
        handler = self.new_handler()
        handler+= func

        self.assertIs(func, handler[0])

    def test_can_remove_observer_with_isub_symbol(self):
        func = lambda: True
        handler = self.new_handler(func)
        handler-= func

        self.assertIs(0, len(handler))

    def test_can_add_conditional_observer(self):
        condition = lambda: True
        handler = self.new_handler()
        conditional = handler.when(condition)
        self.assertIs(conditional, handler[0])
        self.assertEqual(condition, conditional.condition)


    def test_can_clear_registered_events(self):
        handler = self.new_handler()
        handler(Event(self))
        handler(Event(self))

        self.assertEqual(2, len(handler.events))

        handler.clear_events()

        self.assertEqual(0, len(handler.events))

    def test_can_clear_events_and_observers(self):
        handler = self.new_handler()
        mock = self.new_callback()

        handler+= mock
        handler(Event(self))
        handler(Event(self))

        self.assertEqual(2, len(handler.events))
        self.assertEqual(1, len(handler))

        handler.clear()

        self.assertEqual(0, len(handler.events))
        self.assertEqual(0, len(handler))


    def test_it_take_an_extra_argument_named_condition(self):
        func = lambda: True
        handler = self.new_handler(condition=func)
        self.assertIs(func, handler.condition)

    def test_condition_must_be_callable(self):
        expected = "not callable"
        with self.assertRaisesRegex(TypeError, expected):
            self.new_handler(condition=expected)

    def test_event_is_not_propagated_if_condition_is_false(self):
        condition = lambda event: False
        func = self.new_callback()
        handler = self.new_handler(func, condition=condition)
        handler(Event(self))

        self.assertIs(0, func.call_count)

    def test_if_an_init_arg_has_visit_attr_it_is_called(self):
        class Visitor(object):
            def __init__(self):
                self.visit = Mock()

        visitor = Visitor()
        obj = self.new_handler(visitor)
        visitor.visit.assert_called_once_with(obj)


    def new_handler(self, *args, **kwargs):
        return Handler(*args, **kwargs)

    def new_callback(self):
        class callback(object):
            call_count = 0
            def __call__(self, *args, **kwargs):
                self.call_count += 1

        return callback()
