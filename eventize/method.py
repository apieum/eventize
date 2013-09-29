# -*- coding: utf8 -*-
from events.events import _EventSlot


class Method(object):
    def __init__(self, func):
        self.__assert_callable(func)
        self.on = _EventSlot('on')
        self.before = _OverrideArgsEventSlot('before')
        self.after = _OverrideResultEventSlot('after')
        self._func = func

    def __call__(self, *args, **kwargs):
        args, kwargs = self.before(*args, **kwargs)
        self.on(*args, **kwargs)
        result = self._func(*args, **kwargs)
        return self.after(result)

    def __assert_callable(self, func):
        if not callable(func):
            raise AttributeError('"%s" is not callable' % func)


class _OverrideArgsEventSlot(_EventSlot):
    def __call__(self, *args, **kwargs):
        for target in self.targets:
            args, kwargs = target(*args, **kwargs)
        return args, kwargs

class _OverrideResultEventSlot(_EventSlot):
    def __call__(self, result):
        for target in self.targets:
            result = target(result)
        return result
