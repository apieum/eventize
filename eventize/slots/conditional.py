# -*- coding: utf8 -*-
from events.events import _EventSlot


class Conditional(_EventSlot):
    def called_with(self, *expected_args, **expected_kwargs):
        def condition(*args, **kwargs):
            for arg in expected_args:
                if arg not in args:
                    return False
            for key, item in expected_kwargs.iteritems():
                if key not in kwargs or kwargs[key] is not item:
                    return False
            return True
        return self.when(condition)

    def when(self, condition):
        return ConditionalCall(self, condition)

class ConditionalCall(object):
    def __init__(self, slot, condition):
        self.slot = slot
        self.condition = condition

    def do(self, func):
        self.slot += lambda *args, **kwargs: self.condition(*args, **kwargs) and func(*args, **kwargs)
