# -*- coding: utf8 -*-
import sys
from .. import TestCase, Mock
from eventize.descriptors import named
from eventize.typing import Modifier as AbstractModifier


class NamedValueTest(TestCase):
    original_Named_ValueType = named.Named.ValueType

    def tearDown(self):
        named.Named.ValueType = self.original_Named_ValueType

    def test_it_can_receive_visitors(self):
        class Modifier(AbstractModifier):
            visit = Mock()

        obj = named.Named(Modifier())
        Modifier.visit.assert_called_once_with(obj)

    def test_find_alias(self):
        class A(object): pass

        obj = named.Named()
        A.obj = obj
        self.assertEqual(obj.find_alias(A), 'obj')

    def test_alias_not_found(self):
        class A(object): pass

        obj = named.Named()
        with self.assertRaises(LookupError):
            obj.find_alias(A)

    def test_find_alias_of_subclass(self):
        class A(object): pass
        class B(A): pass

        obj = named.Named()
        A.obj = obj
        self.assertEqual(obj.find_alias(B), 'obj')

    def test_get_value(self):
        class A(object):
            pass

        named.Named.ValueType = mock = Mock()

        obj = named.Named()
        obj.get_alias = Mock(return_value='obj')

        a = A()
        obj.get_value(a)
        mock.assert_called_once_with(a, 'obj', None)

    if sys.version_info[0] < 3:
        def test_find_alias_old_class(self):
            class A: obj = named.Named()

            obj = named.Named()
            A.obj = obj
            self.assertEqual(obj.find_alias(A), 'obj')

        def test_find_alias_of_old_subclass(self):
            class A: pass
            class B(A): pass

            obj = named.Named()
            A.obj = obj
            self.assertEqual(obj.find_alias(B), 'obj')

        def test_get_value_old_class(self):
            class A: pass

            named.Named.ValueType = mock = Mock()

            obj = named.Named()
            obj.get_alias = Mock(return_value='obj')

            a = A()
            obj.get_value(a)
            mock.assert_called_once_with(a, 'obj', None)
