# -*- coding: utf8 -*-
from .. import Mock, TestCase, call
from eventize.typing import modifiers
from . import testStack

class ModifierAbstractInterfaceTest(TestCase):
    def setUp(self):
        self.visitor = modifiers.Modifier()

    def test_Modifier_has_method_visit(self):
        self.assertTrue(hasattr(self.visitor, 'visit'))

    def test_Modifier_has_method_restore(self):
        self.assertTrue(hasattr(self.visitor, 'restore'))

    def test_Modifier_visit_method_is_not_implemented(self):
        with self.assertRaises(NotImplementedError):
            self.visitor.visit(self)

    def test_Modifier_restore_method_is_not_implemented(self):
        with self.assertRaises(NotImplementedError):
            self.visitor.restore(self)

class ModifierTest(TestCase):
    def test_it_can_visit_multiple_objects(self):
        Visitor = type("Visitor", (modifiers.Modifier, ), {'visit': Mock()})

        expected0, expected1 = Mock(), Mock()
        Visitor().visit_all(expected0, expected1)
        Visitor.visit.assert_has_calls([call(expected0), call(expected1)])
        self.assertEqual(2, Visitor.visit.call_count)

    def test_it_can_restore_multiple_objects(self):
        Visitor = type("Visitor", (modifiers.Modifier, ), {'restore': Mock()})

        expected0, expected1 = Mock(), Mock()
        Visitor().restore_all(expected0, expected1)
        Visitor.restore.assert_has_calls([call(expected0), call(expected1)])
        self.assertEqual(2, Visitor.restore.call_count)


class ModifierDecoratorTest(ModifierTest):
    def setUp(self):
        self.decorate = modifiers.modifier
        self.decorator_type = modifiers.Modifier

    def test_it_returns_an_object_of_Modifier_type(self):
        @self.decorate
        def do_modify(visited):
            pass
        self.assertIsInstance(do_modify, self.decorator_type)

    def test_comparison_is_made_on_visit_function(self):
        do_modify = lambda visited: visited
        do_restore= lambda visited: visited
        given = self.decorate(do_modify, do_restore)
        self.assertEqual(given, do_modify)

    def test_modifier_restore_method_is_a_decorator_which_set_modifier_restore(self):
        @self.decorate
        def do_modify(visited):
            pass

        @do_modify.restore
        def do_restore(visited):
            return 'is restore'

        self.assertEqual(do_modify.restore(self), 'is restore')

    def test_visit_is_not_bound(self):
        expected = Mock()
        @self.decorate
        def do_modify(visited):
            self.assertIs(visited, expected)

        do_modify.visit(expected)


    def test_restore_is_not_bound(self):
        expected = Mock()
        @self.decorate
        def do_modify(visited):
            pass

        @do_modify.restore
        def do_restore(visited):
            self.assertIs(visited, expected)

        do_modify.restore(expected)



class ModifiersTest(ModifierTest, testStack.CheckedStackTest):
    def setUp(self):
        self.refuse = Mock()
        self.reject = Mock()
        self.visitors = modifiers.Modifiers(refuse=self.refuse, reject=self.reject)

    def test_it_is_a_Modifier(self):
        self.assertIsInstance(self.visitors, modifiers.Modifier)

    def test_it_is_a_checked_stack(self):
        self.assertIsInstance(self.visitors, modifiers.stack.Checked)

    def test_it_checks_if_item_is_a_Modifier(self):
        expected_true = modifiers.Modifier()
        expected_false = Mock()
        self.assertTrue(self.visitors.check(expected_true))
        self.assertFalse(self.visitors.check(expected_false))

    def test_accept_calls_visit_on_given_object(self):
        visitor = type("MyVisitor", (modifiers.Modifier, ), {'visit': Mock()})
        self.visitors.accept(self, visitor)
        visitor.visit.assert_called_once_with(self)

    def test_deny_calls_restore_on_given_object(self):
        visitor = type("MyVisitor", (modifiers.Modifier, ), {'restore': Mock()})
        self.visitors.deny(self, visitor)
        visitor.restore.assert_called_once_with(self)

    def test_append_pushes_and_applies_visitor(self):
        myVisitor = type('MyVisitor', (modifiers.Modifier, ), {'visit': Mock()})()

        self.visitors.append(self, myVisitor)
        self.assertIn(myVisitor, self.visitors)
        myVisitor.visit.assert_called_once_with(self)

    def test_even_if_item_is_not_a_modifier_it_contains_it(self):
        item = Mock()
        self.visitors.append(self, item)
        self.assertIn(item, self.visitors)

    def test_if_item_is_not_a_modifier_it_calls_refuse(self):
        item = Mock()
        self.visitors.append(self, item)
        self.refuse.assert_called_once_with(self, item)

    def test_if_item_is_not_a_modifier_it_is_stored_as_RejectedModifier(self):
        item = Mock()
        self.visitors.append(self, item)
        self.assertIsInstance(self.visitors[0], modifiers.RejectedModifier)

    def test_when_visit_it_calls_its_items_visit_method(self):
        visitor0 = type('MyVisitor', (modifiers.Modifier, ), {'visit': Mock()})()
        visitor1 = type('MyVisitor', (modifiers.Modifier, ), {'visit': Mock()})()
        self.visitors.push(visitor0)
        self.visitors.push(visitor1)
        self.visitors.visit(self)
        visitor0.visit.assert_called_once_with(self)
        visitor1.visit.assert_called_once_with(self)

    def test_visit_is_applied_in_push_order(self):
        given = list()
        class MyVisitor(modifiers.Modifier):
            def visit(self, visited):
                given.append(self)

        visitor0 = MyVisitor()
        visitor1 = MyVisitor()
        self.visitors.push(visitor0)
        self.visitors.push(visitor1)
        self.visitors.visit(self)
        self.assertIs(given[0], visitor0)
        self.assertIs(given[1], visitor1)


    def test_when_restore_it_calls_its_items_restore_method(self):
        visitor0 = type('MyVisitor', (modifiers.Modifier, ), {'restore': Mock()})()
        visitor1 = type('MyVisitor', (modifiers.Modifier, ), {'restore': Mock()})()
        self.visitors.push(visitor0)
        self.visitors.push(visitor1)
        self.visitors.restore(self)
        visitor0.restore.assert_called_once_with(self)
        visitor1.restore.assert_called_once_with(self)


    def test_restore_is_applied_in_push_reversed_order(self):
        given = list()
        class MyVisitor(modifiers.Modifier):
            def restore(self, visited):
                given.append(self)

        visitor0 = MyVisitor()
        visitor1 = MyVisitor()
        self.visitors.push(visitor1)
        self.visitors.push(visitor0)
        self.visitors.restore(self)
        self.assertIs(given[0], visitor0)
        self.assertIs(given[1], visitor1)

    def test_rollbackto_restore_visited_object_state_and_remove_visitors(self):
        class MyObject(object):
            def __init__(self):
                self.count = 1
                self.coef = 1

        class MyVisitor(modifiers.Modifier):
            def visit(self, visited):
                visited.coef*=3
                visited.count+= visited.coef

            def restore(self, visited):
                visited.count-= visited.coef
                visited.coef/=3

        visitor = MyVisitor()
        visited = MyObject()
        self.visitors.push(visitor)
        self.visitors.push(visitor)
        self.visitors.visit(visited)
        self.assertEqual(2, len(self.visitors))
        self.assertEqual(visited.count, 13)
        self.visitors.rollback_to(visited, 1)
        self.assertEqual(visited.count, 4)
        self.assertEqual(1, len(self.visitors))


    def test_rollback_restore_visited_object_state_and_remove_visitors(self):
        class MyObject(object):
            def __init__(self):
                self.count = 1
                self.coef = 1

        class MyVisitor(modifiers.Modifier):
            def visit(self, visited):
                visited.coef*=3
                visited.count+= visited.coef

            def restore(self, visited):
                visited.count-= visited.coef
                visited.coef/=3

        visitor0 = MyVisitor()
        visitor1 = MyVisitor()
        visited = MyObject()
        self.visitors.push(visitor0)
        self.visitors.push(visitor1)
        self.visitors.visit(visited)
        self.assertEqual(2, len(self.visitors))
        self.assertEqual(visited.count, 13)
        self.visitors.rollback(visited, visitor1)
        self.assertEqual(visited.count, 4)
        self.assertEqual(1, len(self.visitors))

    def test_expunge_visitor_make_as_if_it_was_never_added(self):
        class MyObject(object):
            def __init__(self):
                self.count = 1

        class AddMul(modifiers.Modifier):
            def __init__(self, add, mul):
                self.add = add
                self.mul = mul
            def visit(self, visited):
                visited.count+= self.add
                visited.count*= self.mul

            def restore(self, visited):
                visited.count/= self.mul
                visited.count-= self.add

        visitor0 = AddMul(1, 2)
        visitor1 = AddMul(2, 3)
        visited = MyObject()
        self.visitors.push(visitor0)
        self.visitors.push(visitor1)
        self.visitors.visit(visited)
        self.assertEqual(2, len(self.visitors))
        self.assertEqual(visited.count, 18)
        self.visitors.expunge(visited, visitor0)
        self.assertEqual(visited.count, 9)
        self.assertEqual(1, len(self.visitors))

