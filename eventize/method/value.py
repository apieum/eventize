# -*- coding: utf8 -*-
from ..descriptors import value
from .handler import Handler, Subject, InstanceHandler
from .event import BeforeEvent, AfterEvent


class Value(value.Value):
    event_types = {
        'before': BeforeEvent,
        'after': AfterEvent
    }
    def set_handlers(self):
        self.before = InstanceHandler()
        self.after = InstanceHandler()

    def init_value(self, value):
        def func(*args, **kwargs):
            event = self.notify('before', self, *args, **kwargs)
            event.call(self.__func__)
            return self.notify('after', event).returns()

        setattr(func, '__name__', self.name)
        self.data = func
        return value

    def set(self, value):
        self._assert_callable(value)
        self.__func__ = value
        setattr(self.get(), '__func__', value)

    def delete(self):
        delattr(self, self.__func__)

    def _assert_callable(self, func):
        if not callable(func):
            raise AttributeError('"%s" is not callable' % func)
