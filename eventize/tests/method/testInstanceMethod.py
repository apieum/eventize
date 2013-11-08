# -*- coding: utf8 -*-
from .. import TestCase
from eventize.method.descriptor import MethodInstance

class InstanceMethodTest(TestCase):

    def test_InstanceMethod_is_a_callable_object(self):
        self.assertTrue(callable(MethodInstance))
