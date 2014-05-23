# -*- coding: utf8 -*-
from ..descriptors import value
from .handler import Before, After

class Value(value.Value):
    def set_handlers(self):
        self.before = Before()
        self.after = After()

    def init_value(self, value):
        def func(*args, **kwargs):
            event = self.notify('before', self, *args, **kwargs)
            event.call(self.__func__)
            return self.notify('after', event).returns()

        setattr(func, '__name__', self.name)
        setattr(self, 'data', func)
        self.set(value)

    def set(self, value):
        self._assert_callable(value)
        self.__func__ = value
        setattr(self.get(), '__func__', value)

    def delete(self):
        delattr(self, self.__func__)

    def _assert_callable(self, func):
        if not callable(func):
            raise AttributeError('"%s" is not callable' % func)
