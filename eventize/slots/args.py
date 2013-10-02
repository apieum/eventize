# -*- coding: utf8 -*-
from conditional import Conditional

class OverrideArgs(Conditional):
    def __call__(self, *args, **kwargs):
        for target in self.targets:
            args, kwargs = target(*args, **kwargs)
        return args, kwargs
