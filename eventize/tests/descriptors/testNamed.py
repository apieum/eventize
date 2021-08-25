# -*- coding: utf8 -*-
from .. import TestCase, Mock
from eventize.descriptors import named
from eventize.typing import Modifier as AbstractModifier


class NamedValueTest(TestCase):
    def test_it_can_receive_visitors(self):
        class Modifier(AbstractModifier):
            visit = Mock()

        obj = named.Named(Modifier())
        Modifier.visit.assert_called_once_with(obj)

    def test_find_alias(self):
        class A: pass

        obj = named.Named()
        A.obj = obj
        self.assertEqual(obj.find_alias(A), 'obj')

    def test_alias_not_found(self):
        class A: pass

        obj = named.Named()
        with self.assertRaises(LookupError):
            obj.find_alias(A)

    def test_find_alias_of_subclass(self):
        class A: pass
        class B(A): pass

        obj = named.Named()
        A.obj = obj
        self.assertEqual(obj.find_alias(B), 'obj')
