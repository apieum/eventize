# -*- coding: utf8 -*-
from slot import Slot


class OverrideResult(Slot):
    def propagate(self, result):
        for func in self:
            result = func(result)
        return result
