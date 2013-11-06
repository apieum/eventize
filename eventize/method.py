# -*- coding: utf8 -*-
from .namedDescriptor import NamedDescriptor
from .events.handler import MethodHandler, Handler
from .events.event import MethodEvent


class Method(NamedDescriptor):
    before = MethodHandler()
    after = MethodHandler()

    def __init__(self, func):
        self._assert_callable(func)
        self.__func__ = func

    def __call__(self, *args, **kwargs):
        event = self.before.call(self, *args, **kwargs)
        event.call(self.__func__)
        self.after(event)
        return event.returns()

    def get(self, instance, name):
        if self._is_not_bound(name, instance):
            self._bind_method(name, instance)
        return instance.__dict__[name]

    def _bind_method(self, name, instance):
        def method(*args, **kwargs):
            event = instance.__dict__[name].before.call(instance, *args, **kwargs)
            event.call(self.__func__)
            instance.__dict__[name].after(event)
            return event.returns()

        method.__name__ = name
        method.before = Handler()
        method.after = Handler()
        method.before.event_class = MethodEvent
        method.after.event_class = MethodEvent
        instance.__dict__[name] = method

    def _is_not_bound(self, name, instance):
        return not (hasattr(instance, '__dict__') and name in instance.__dict__)

    def _assert_callable(self, func):
        if not callable(func):
            raise AttributeError('"%s" is not callable' % func)
