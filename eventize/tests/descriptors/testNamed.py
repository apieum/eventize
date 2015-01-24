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





