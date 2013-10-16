# -*- coding: utf8 -*-
from .namedDescriptor import NamedDescriptor
from .events.handler import BeforeHandler, AfterHandler


class Method(NamedDescriptor):
    before = BeforeHandler()
    after = AfterHandler()

    def __init__(self, func):
        self._assert_callable(func)
        self.__func__ = func
        self._set_func_properties(self, func)

    def __call__(self, *args, **kwargs):
        event = self.before(self, *args, **kwargs)
        event.call(self.__func__)
        self.after.trigger(event)
        return event.result

    def get(self, instance, name):
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
            event = instance.__dict__[name].before(instance, *args, **kwargs)
            event.call(self.__func__)
            instance.__dict__[name].after.trigger(event)
            return event.result

        method.__name__ = name
        self._set_func_properties(method, self.__func__)
        method.before = BeforeHandler(self.before)
        method.after = AfterHandler(self.after)
        instance.__dict__[name] = method

    def _is_not_bound(self, name, instance):
        return not hasattr(instance, '__dict__') or name not in instance.__dict__

    def _assert_callable(self, func):
        if not callable(func):
            raise AttributeError('"%s" is not callable' % func)
