# -*- coding: utf8 -*-
from .events import Listener
from .namedDescriptor import NamedDescriptor


class Method(NamedDescriptor, Listener):
    __events__ = ['before', 'after']
    def __init__(self, func):
        self._assert_callable(func)
        self.__func__ = func
        self._set_func_properties(self, func)

        self._set_events(self)

    def __call__(self, *args, **kwargs):
        event = self._make_event(self, *args, **kwargs)
        event.subject.before(event)
        event.call(self.__func__)
        event.subject.after(event)
        return event.result

    def get(self, name, instance):
        if self._is_not_bound(name, instance):
            self._bind_method(name, instance)

        return instance.__dict__[name]

    def _set_func_properties(self, instance, func):
        if not hasattr(func, '__name__'):
            func = func.__call__

        instance.__doc__ = getattr(func, '__doc__', '')
        instance.__defaults__ = getattr(func, '__defaults__', None)


    def _bind_method(self, name, instance):
        def method(*args, **kwargs):
            event = self._make_event(instance, *args, **kwargs)
            event.subject.__dict__[name].before(event)
            event.call(self.__func__)
            event.subject.__dict__[name].after(event)
            return event.result

        method.__name__ = name
        self._set_func_properties(method, self.__func__)
        instance.__dict__[name] = self._set_events(method)
        instance.__dict__[name].before += self.before
        instance.__dict__[name].after += self.after

    def _is_not_bound(self, name, instance):
        return name not in instance.__dict__

    def _assert_callable(self, func):
        if not callable(func):
            raise AttributeError('"%s" is not callable' % func)
