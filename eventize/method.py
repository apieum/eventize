# -*- coding: utf8 -*-
from .events import Listener
from .namedDescriptor import NamedDescriptor


class Method(NamedDescriptor, Listener):
    __events__ = ['before', 'after']
    def __init__(self, func):
        self._assert_callable(func)
        self.__func__ = func
        self._define_func_properties(func)

        self._set_events(self)

    def __call__(self, *args, **kwargs):
        event = self._make_event(self, *args, **kwargs)
        self.trigger('before', event)
        event.call(self.__func__)
        self.trigger('after', event)
        return event.result

    def _retrieve_from_name(self, name, instance):
        if self._is_not_bound(name, instance):
            self._bind_method(name, instance)

        return instance.__dict__[name]

    def _define_func_properties(self, func):
        if not hasattr(func, '__name__'):
            func = func.__call__

        self.__doc__ = getattr(func, '__doc__', '')
        self.__defaults__ = getattr(func, '__defaults__', None)
        self.__code__ = getattr(func, '__code__', None)


    def _bind_method(self, name, instance):
        get_trigger = lambda event: getattr(event.instance.__dict__[name], 'trigger', self._null_trigger)
        def method(*args, **kwargs):
            event = self._make_event(instance, *args, **kwargs)
            trigger = get_trigger(event)
            trigger('before', event)
            event.call(self.__func__)
            trigger('after', event)
            return event.result

        method.__name__ = name
        instance.__dict__[name] = self._set_events(method)

    def _is_not_bound(self, name, instance):
        return name not in instance.__dict__

    def _assert_callable(self, func):
        if not callable(func):
            raise AttributeError('"%s" is not callable' % func)
