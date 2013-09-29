# -*- coding: utf8 -*-
from events.events import _EventSlot

class OverrideArgs(_EventSlot):
    def __call__(self, *args, **kwargs):
        for target in self.targets:
            args, kwargs = target(*args, **kwargs)
        return args, kwargs