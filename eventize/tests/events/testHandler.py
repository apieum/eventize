# -*- coding: utf8 -*-
from .. import TestCase, Mock
from eventize.events import Expect, Handler
from eventize.method import Event


class EventHandlerTest(TestCase):
    def test_a_Handler_is_callable(self):
        handler = self.new_handler()
        self.assertTrue(callable(handler))

    def test_a_Handler_is_a_list_of_callable(self):
        handler = self.new_handler()
        handler.append(Mock())
        handler.append(Mock())
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
        handler.append(Mock())
        with self.assertRaisesRegex(TypeError, 'string'):
            handler[0] = 'string'

    def test_when_an_handler_is_called_all_its_contents_is_called(self):
        mock1 = Mock()
        mock2 = Mock()
        handler = self.new_handler()
        handler.append(mock1)
        handler.append(mock2)
        event = Event(self)
        handler(event)

        mock1.assert_called_once_with(event)
        mock2.assert_called_once_with(event)

    def test_when_an_observer_raises_StopPropagation_following_observers_are_not_executed(self):
        def func1(event):
            event.stop_propagation()

        mock = Mock()
        handler = self.new_handler()
        handler.append(func1)
        handler.append(mock)
        handler(Event(self))

        self.assertEqual(0, mock.call_count)

    def test_Handler_arguments_is_the_list_content(self):
        expected1 = Mock()
        expected2 = Mock()
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
        handler = self.new_handler(Mock(), Mock())
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

    def test_can_add_condition_about_args(self):
        func = Mock()
        handler = self.new_handler()
        event1 = Event(self, valid=True)
        event2 = Event(self, valid=False)
        handler.when(Expect.kwargs(valid=True)).do(func)
        handler(event1)
        handler(event2)
        func.assert_called_once_with(event1)


    def test_called_with_make_a_condition_func_about_args_and_kwargs(self):
        handler = self.new_handler()
        expected_args = ('args', )
        expected_kwargs = {'kwarg':'kwarg'}
        args_and_kwargs = Expect.args(*expected_args) & Expect.kwargs(**expected_kwargs)
        conditional = handler.when(args_and_kwargs)
        event = Event(self, *expected_args, **expected_kwargs)
        self.assertTrue(conditional.condition(event))
        event.args = ('arg1',)
        self.assertFalse(conditional.condition(event))

    def test_can_clear_registered_events(self):
        handler = self.new_handler()
        handler(Event(self))
        handler(Event(self))

        self.assertEqual(2, len(handler.events))

        handler.clear_events()

        self.assertEqual(0, len(handler.events))

    def test_can_clear_events_and_observers(self):
        handler = self.new_handler()
        mock = Mock()

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
        func = Mock()
        handler = self.new_handler(func, condition=condition)
        handler(Event(self))

        self.assertIs(0, func.call_count)

    def new_handler(self, *args, **kwargs):
        return Handler(*args, **kwargs)
