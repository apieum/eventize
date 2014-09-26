# -*- coding: utf8 -*-
from .. import TestCase, Mock
from eventize.descriptors import named
from eventize.typing import Visitor as AbstractVisitor

class NamedValueTest(TestCase):
    def test_it_can_receive_visitors(self):
        class Visitor(AbstractVisitor):
            visit = Mock()

        visitor = Visitor()
        obj = named.Named(visitor)
        visitor.visit.assert_called_once_with(obj)





