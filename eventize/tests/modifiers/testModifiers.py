# -*- coding: utf8 -*-
from .. import TestCase, Mock
from eventize.typing.modifiers import *

class MyVisitable(Visitable):
    def reject(self, visitor):
        setattr(visitor, 'rejected', True)

class MyModifiable(Modifiable):
    def reject(self, visitor):
        setattr(visitor, 'rejected', True)
    def defer(self, visitor):
        setattr(visitor, 'deferred', True)

class VisitorTest(TestCase):
    def test_when_accept_visitor_it_calls_its_visit_method(self):
        class MyVisitor(Visitor):
            visit = Mock()
        expected = MyVisitable()
        visitor = MyVisitor()
        expected.accept(visitor)
        visitor.visit.assert_called_once_with(expected)

    def test_when_accepted_visitor_is_appended_to_visitors_attr(self):
        class MyVisitor(Visitor):
            visit = Mock()
        given = MyVisitable()
        expected = MyVisitor()
        given.accept(expected)
        self.assertIs(expected, given.visitors[0])

    def test_accept_rejects_non_Visitor(self):
        class MyVisitor(object):
            rejected = False
            visit = Mock()
        visitor = MyVisitor()
        MyVisitable().accept(visitor)
        self.assertFalse(visitor.visit.called, 'visit called')
        self.assertTrue(visitor.rejected, 'Visitor not rejected')

    def test_when_rejected_visitor_is_not_appended_to_visitors_attr(self):
        class MyVisitor(object):
            visit = Mock()
        given = MyVisitable()
        expected = MyVisitor()
        given.accept(expected)
        self.assertNotIn(expected, given.visitors)

    def test_accept_all_calls_accept_for_all_arguments(self):
        class MyVisitor(Visitor):
            visit = Mock()
        given = MyVisitable()
        given.accept_all(MyVisitor(), MyVisitor(), MyVisitor())
        self.assertEqual(3, MyVisitor.visit.call_count)

class ModifierTest(TestCase):
    def test_when_expunge_visitor_it_calls_its_restore_method(self):
        class MyVisitor(Modifier):
            visit = Mock()
            restore = Mock()
        expected = MyModifiable()
        visitor = MyVisitor()
        expected.accept(visitor)
        expected.expunge(visitor)
        visitor.restore.assert_called_once_with(expected)

    def test_when_expunge_visitor_is_removed_from_visitors_attr(self):
        class MyVisitor(Modifier):
            visit = Mock()
            restore = Mock()
        modifiable = MyModifiable()
        visitor = MyVisitor()
        modifiable.accept(visitor)
        self.assertIn(visitor, modifiable.visitors)
        modifiable.expunge(visitor)
        self.assertNotIn(visitor, modifiable.visitors)

    def test_expunge_defers_non_Modifiable(self):
        class MyVisitor(Visitor):
            rejected = False
            visit = Mock()
            restore = Mock()
        visitor = MyVisitor()
        modifiable = MyModifiable()
        modifiable.accept(visitor)
        modifiable.expunge(visitor)
        self.assertFalse(visitor.restore.called, 'restore called')
        self.assertFalse(visitor.rejected, 'Visitor rejected')
        self.assertTrue(visitor.deferred, 'Visitor not deffered')

    def test_when_deferred_visitor_is_not_remove_from_visitors_attr(self):
        class MyVisitor(Visitor):
            visit = Mock()
        given = MyModifiable()
        expected = MyVisitor()
        given.accept(expected)
        given.expunge(expected)
        self.assertIs(expected, given.visitors[0])

    def test_rollback_restore_all_visitors_until_given_found(self):
        class MyVisitor(Modifier):
            visit = Mock()
            restore = Mock()
        given = MyModifiable()
        visitor1 = MyVisitor()
        visitor2 = MyVisitor()
        given.accept_all(visitor1, visitor2)
        given.rollback(visitor1)
        self.assertIs(tuple(), given.visitors)

    def test_deny_set_modifiable_to_its_state_without_given_visitor(self):
        class MyVisitor(Modifier):
            def __init__(self, add):
                self.add = add
            def visit(self, modifiable):
                modifiable.value = modifiable.value * 3 + self.add

            def restore(self, modifiable):
                modifiable.value = (modifiable.value - self.add) / 3

        given = MyModifiable()
        given.value = 1
        visitor1 = MyVisitor(2)
        visitor2 = MyVisitor(5)
        given.accept_all(visitor1, visitor2)
        self.assertEqual((1 * 3 + 2) * 3 + 5, given.value)
        given.deny(visitor1)
        self.assertEqual(1 * 3 + 5, given.value)

