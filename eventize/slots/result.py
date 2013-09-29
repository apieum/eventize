# -*- coding: utf8 -*-
from events.events import _EventSlot


class OverrideResult(_EventSlot):
    def __call__(self, result):
        for target in self.targets:
            result = target(result)
        return result
