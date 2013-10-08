# -*- coding: utf8 -*-
from .events import EventSlot, Event
from .namedDescriptor import NamedDescriptor

class Method(NamedDescriptor):
    def __init__(self, func):
        self._assert_callable(func)
        self.__func__ = func
        self._define_func_properties(func)

        events = self._set_events('__call__', self)
        self._bind_events(events, self)

    def __call__(self, *args, **kwargs):
        return self.__dict__['__call__'](*args, **kwargs)

    def __get__(self, instance, ownerCls):
        if instance is None: return self

        name = self._get_name(instance)
        if self._is_not_bound(instance):
            self._bind_method(name, instance)

        return instance.__dict__[self.__name__]

    def _define_func_properties(self, func):
        if not hasattr(func, '__name__'):
            func = func.__call__

        self.__doc__ = getattr(func, '__doc__', '')
        self.__defaults__ = getattr(func, '__defaults__', None)
        self.__code__ = getattr(func, '__code__', None)


    def _bind_method(self, name, instance):
        events = self._set_events(name, instance)
        self._bind_events(events, instance.__dict__[name])

    def _bind_events(self, events, container):
        for event_name, event in events.items():
            setattr(container, event_name, event)
        return container

    def _set_events(self, name, instance):
        before = EventSlot()
        after = EventSlot()
        def method(*args, **kwargs):
            event = Event(instance, *args, **kwargs)
            before(event)
            event.call(self.__func__)
            after(event)
            return event.result

        method.__name__ = name
        instance.__dict__[name] = method
        return {'after': after, 'before': before}

    def _is_not_bound(self, instance):
        return self.__name__ not in instance.__dict__


    def _assert_callable(self, func):
        if not callable(func):
            raise AttributeError('"%s" is not callable' % func)
