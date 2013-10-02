# -*- coding: utf8 -*-
from conditional import Conditional


class OverrideResult(Conditional):
    def __call__(self, result):
        for target in self.targets:
            result = target(result)
        return result
