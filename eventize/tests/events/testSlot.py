# -*- coding: utf8 -*-
import unittest
from mock import Mock
from eventize.events.slot import Slot, StopPropagation

class EventSlotTest(unittest.TestCase):
    def test_a_Slot_is_callable(self):
        slot = self.new_slot()
        self.assertTrue(callable(slot))

    def test_a_Slot_is_a_list_of_callable(self):
        slot = self.new_slot()
        slot.append(Mock())
        slot.append(Mock())
        self.assertEqual(len(slot), 2)

    def test_a_Slot_raise_an_error_when_appending_a_non_callable_item(self):
        slot = self.new_slot()
        with self.assertRaisesRegexp(TypeError, 'string'):
            slot.append('string')

    def test_a_Slot_raise_an_error_when_setting_a_non_callable_item(self):
        slot = self.new_slot()
        slot.append(Mock())
        with self.assertRaisesRegexp(TypeError, 'string'):
            slot[0] = 'string'

    def test_when_a_slot_is_called_all_its_contents_is_called(self):
        mock1 = Mock()
        mock2 = Mock()
        slot = self.new_slot()
        slot.append(mock1)
        slot.append(mock2)
        slot()

        mock1.assert_called_once_with()
        mock2.assert_called_once_with()

    def test_when_an_observer_raises_StopPropagation_following_observers_are_not_executed(self):
        def func1():
            raise StopPropagation()

        mock = Mock()
        slot = self.new_slot()
        slot.append(func1)
        slot.append(mock)
        slot()

        self.assertEqual(0, mock.call_count)

    def test_slot_arguments_is_the_list_content(self):
        expected1 = Mock()
        expected2 = Mock()
        slot = self.new_slot(expected1, expected2)

        self.assertIs(slot[0], expected1)
        self.assertIs(slot[1], expected2)

    def test_cannot_append_non_callable_by_slot_arguments(self):
        expected_exception = 'invalid value 10'
        with self.assertRaisesRegexp(TypeError, expected_exception):
            self.new_slot(expected_exception)

    def test_cannot_append_non_callable_by_slot_extend(self):
        expected_exception = 'invalid value 20'
        slot = self.new_slot()
        with self.assertRaisesRegexp(TypeError, expected_exception):
            slot.extend([expected_exception])

    def test_cannot_append_non_callable_by_slot_insert(self):
        expected_exception = 'invalid value 30'
        slot = self.new_slot(Mock(), Mock())
        with self.assertRaisesRegexp(TypeError, expected_exception):
            slot.insert(0, expected_exception)

    def test_when_propagation_is_stopped_slot_contains_message(self):
        expected = 'message'
        def func():
            raise StopPropagation(expected)

        slot = self.new_slot(func)
        slot()

        self.assertEqual(slot.message, expected)

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
        slot = self.new_slot()
        slot.called_with(valid=True).append(func)
        slot(valid=False)
        slot(valid=True)
        func.assert_called_once_with(valid=True)


    def new_slot(self, *args):
        return Slot(*args)
