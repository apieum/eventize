# -*- coding: utf8 -*-
from slot import Slot

class OverrideArgs(Slot):
    def propagate(self, *args, **kwargs):
        for func in self:
            args, kwargs = func(*args, **kwargs)
        return args, kwargs
