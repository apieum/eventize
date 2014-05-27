# -*- coding: utf8 -*-
from .. import TestCase, Mock
from eventize.descriptors import named

class NamedValueTest(TestCase):
    def test_it_can_receive_visitors(self):
        class Visitor(object):
            def __init__(self):
                self.visit = Mock()

        visitor = Visitor()
        obj = named.Named(visitor)
        visitor.visit.assert_called_once_with(obj)





