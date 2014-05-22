# -*- coding: utf8 -*-
from .. import TestCase, Mock
from eventize.method import Handler, BeforeEvent
from eventize.events import Expect

class MethodHandlerTest(TestCase):

    def test_can_add_condition_about_args(self):
        func = Mock()
        self.instance = self.new_handler()
        event1 = BeforeEvent(self, valid=True)
        event2 = BeforeEvent(self, valid=False)
        self.instance.when(Expect.kwargs(valid=True)).do(func)
        self.instance(event1)
        self.instance(event2)
        func.assert_called_once_with(event1)

    def new_handler(self, *args, **kwargs):
        return Handler(*args, **kwargs)
