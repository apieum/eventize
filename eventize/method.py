# -*- coding: utf8 -*-
from slots import OverrideArgs, OverrideResult, Conditional

class Method(object):
    def __init__(self, func):
        self.__assert_callable(func)
        self.on = Conditional('on')
        self.before = OverrideArgs('before')
        self.after = OverrideResult('after')
        self._func = func

    def __call__(self, *args, **kwargs):
        args, kwargs = self.before(*args, **kwargs)
        self.on(*args, **kwargs)
        result = self._func(*args, **kwargs)
        return self.after(result)

    def __assert_callable(self, func):
        if not callable(func):
            raise AttributeError('"%s" is not callable' % func)
