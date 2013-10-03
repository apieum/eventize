# -*- coding: utf8 -*-
from slot import Slot


class Conditional(Slot):
    def __init__(self, *args, **kwargs):
        Slot.__init__(self, *args)
        if 'condition' not in kwargs:
            kwargs['condition'] = lambda *args, **kwargs: True
        self._assert_valid(kwargs['condition'])
        self.condition = kwargs['condition']


    def propagate(self, args, kwargs):
        result = None
        if not self.condition(*args, **kwargs):
            return result
        for func in self:
            result = func(*args, **kwargs)
        return result

    def do(self, func):
        self.append(func)
