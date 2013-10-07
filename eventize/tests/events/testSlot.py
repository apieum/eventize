# -*- coding: utf8 -*-
from eventize.tests import TestCase, Mock
from eventize.events.slot import Slot
from eventize.events.event import Event

class EventSlotTest(TestCase):
    def test_a_Slot_is_callable(self):
        slot = self.new_slot()
        self.assertTrue(callable(slot))

    def test_a_Slot_is_a_list_of_callable(self):
        slot = self.new_slot()
        slot.append(Mock())
        slot.append(Mock())
        self.assertEqual(len(slot), 2)

    def test_do_method_is_same_as_append(self):
        slot = self.new_slot()
        self.assertEqual(slot.append, slot.do)

    def test_a_Slot_raise_an_error_when_appending_a_non_callable_item(self):
        slot = self.new_slot()
        with self.assertRaisesRegex(TypeError, 'string'):
            slot.append('string')

    def test_a_Slot_raise_an_error_when_setting_a_non_callable_item(self):
        slot = self.new_slot()
        slot.append(Mock())
        with self.assertRaisesRegex(TypeError, 'string'):
            slot[0] = 'string'

    def test_when_a_slot_is_called_all_its_contents_is_called(self):
        mock1 = Mock()
        mock2 = Mock()
        event = Event(self)
        slot = self.new_slot()
        slot.append(mock1)
        slot.append(mock2)
        slot(event)

        mock1.assert_called_once_with(event)
        mock2.assert_called_once_with(event)

    def test_when_an_observer_raises_StopPropagation_following_observers_are_not_executed(self):
        def func1(event):
            event.stop_propagation()

        mock = Mock()
        slot = self.new_slot()
        slot.append(func1)
        slot.append(mock)
        event = Event(self)
        slot(event)

        self.assertEqual(0, mock.call_count)

    def test_slot_arguments_is_the_list_content(self):
        expected1 = Mock()
        expected2 = Mock()
        slot = self.new_slot(expected1, expected2)

        self.assertIs(slot[0], expected1)
        self.assertIs(slot[1], expected2)

    def test_cannot_append_non_callable_by_slot_arguments(self):
        expected_exception = 'invalid value 10'
        with self.assertRaisesRegex(TypeError, expected_exception):
            self.new_slot(expected_exception)

    def test_cannot_append_non_callable_by_slot_extend(self):
        expected_exception = 'invalid value 20'
        slot = self.new_slot()
        with self.assertRaisesRegex(TypeError, expected_exception):
            slot.extend([expected_exception])

    def test_cannot_append_non_callable_by_slot_insert(self):
        expected_exception = 'invalid value 30'
        slot = self.new_slot(Mock(), Mock())
        with self.assertRaisesRegex(TypeError, expected_exception):
            slot.insert(0, expected_exception)

    def test_when_propagation_is_stopped_event_contains_message(self):
        expected = 'message'
        def func(event):
            event.stop_propagation(expected)

        slot = self.new_slot(func)
        event = Event(self)
        slot(event)

        self.assertEqual(event.messages[0], expected)

    def test_can_append_observer_with_iadd_symbol(self):
        func = lambda: True
        slot = self.new_slot()
        slot+= func

        self.assertIs(func, slot[0])

    def test_can_remove_observer_with_isub_symbol(self):
        func = lambda: True
        slot = self.new_slot(func)
        slot-= func

        self.assertIs(0, len(slot))

    def test_can_add_conditional_observer(self):
        condition = lambda: True
        slot = self.new_slot()
        conditional = slot.when(condition)
        self.assertIs(conditional, slot[0])
        self.assertEqual(condition, conditional.condition)

    def test_can_add_condition_about_args(self):
        func = Mock()
        event1 = Event(self, valid=True)
        event2 = Event(self, valid=False)
        slot = self.new_slot()
        slot.called_with(valid=True).do(func)
        slot(event1)
        slot(event2)
        func.assert_called_once_with(event1)


    def test_called_with_make_a_condition_func_about_args_nd_kwargs(self):
        slot = self.new_slot()
        expected_args = ('args', )
        expected_kwargs = {'kwarg':'kwarg'}
        conditional = slot.called_with(*expected_args, **expected_kwargs)
        event = Event(self, *expected_args, **expected_kwargs)
        self.assertTrue(conditional.condition(event))
        event.args = ('arg1',)
        self.assertFalse(conditional.condition(event))

    def test_can_remove_all_registered_events(self):
        slot = self.new_slot()
        event = Event(self)
        slot(event)
        slot(event)

        self.assertEqual(2, len(slot.events))

        slot.remove_events()

        self.assertEqual(0, len(slot.events))

    def test_can_remove_all_events_and_observers(self):
        slot = self.new_slot()
        event = Event(self)
        mock = Mock()

        slot+= mock
        slot(event)
        slot(event)

        self.assertEqual(2, len(slot.events))
        self.assertEqual(1, len(slot))

        slot.remove_all()

        self.assertEqual(0, len(slot.events))
        self.assertEqual(0, len(slot))

    def new_slot(self, *args):
        return Slot(*args)
