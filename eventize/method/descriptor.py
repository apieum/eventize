# -*- coding: utf8 -*-
from .. import descriptors
from .handler import Handler, Subject, InstanceHandler
from .event import Event


class Value(descriptors.Value):
    def set_handlers(self):
        self.before = InstanceHandler()
        self.after = InstanceHandler()

    def init_value(self, value):
        def func(*args, **kwargs):
            event = Event(self.instance, *args, **kwargs)
            self.notify('before', event)
            event.call(self.__func__)
            self.notify('after', event)
            return event.returns()

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


@Subject
class Descriptor(descriptors.Named):
    ValueType = Value
    before = Handler()
    after = Handler()

