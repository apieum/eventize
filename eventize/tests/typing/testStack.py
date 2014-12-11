# -*- coding: utf8 -*-
from .. import TestCase, Mock
from eventize.typing import CheckedStack

return_true = lambda item: True

class CheckedStackTest(TestCase):
    def test_push_appends_items_from_left(self):
        item1, item2 = Mock(), Mock()
        stack = CheckedStack(check=return_true)
        stack.push(item1)
        stack.push(item2)
        self.assertIs(item2, stack[0])

    def test_init_appends_args_in_reverse_order(self):
        item1, item2 = Mock(), Mock()
        stack = CheckedStack([item1, item2], check=return_true)
        self.assertIs(item2, stack[0])

    def test_can_push_multiple_items(self):
        item1, item2 = Mock(), Mock()
        stack = CheckedStack(check=return_true)
        stack.push_all(item1, item2)
        self.assertIs(item2, stack[0])

    def test_can_get_item_index(self):
        item1, item2 = Mock(), Mock()
        stack = CheckedStack(check=return_true)
        stack.push_all(item1, item2)
        self.assertIs(stack.index(item2), 0)
        self.assertIs(stack.index(item1), 1)

    def test_cant_push_item_if_check_return_false(self):
        stack = CheckedStack(check=lambda item: False)
        with self.assertRaises(NotImplementedError) as exception:
            stack.push(Mock())

    def test_push_call_fallback_if_check_return_false(self):
        item1 = Mock()
        fallback = Mock(return_value=item1)
        stack = CheckedStack(check=lambda item: False, fallback=fallback)
        stack.push(item1)
        fallback.assert_called_once_with(item1)
        self.assertIn(item1, stack)

    def test_push_call_fallback_method_if_check_return_false(self):
        class Stack(CheckedStack):
            called = False
            def fallback(self, item):
                self.called = True
                return item
            def check(self, item):
                return False
        item1 = Mock()
        stack = Stack()
        stack.push(item1)
        self.assertTrue(stack.called, "Stack.fallback not called")
        self.assertIn(item1, stack)

    def test_it_removes_the_first_found_item(self):
        item1, item2 = Mock(), Mock()
        stack = CheckedStack([item1, item2, item1], check=return_true)
        stack.remove(item1)
        self.assertIs(item2, stack[0])
        self.assertIs(2, len(stack))

