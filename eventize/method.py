# -*- coding: utf8 -*-
from events import OverrideArgs, OverrideResult, EventSlot


class Method(object):
    def __init__(self, func):
        self._assert_callable(func)

        self.func_name = getattr(func, 'func_name', 'method')
        self.func_doc = getattr(func, 'func_doc', '')
        self.__func__ = func

        events = self._set_events('__call__', self)
        self._bind_events(events, self)

    def __call__(self, *args, **kwargs):
        return self.__dict__['__call__'](*args, **kwargs)

    def __get__(self, instance, ownerCls):
        if instance is None: return self

        if self._is_not_bound(instance):
            self._bind_method(self.func_name, instance)

        return instance.__dict__[self.func_name]

    def _bind_method(self, name, instance):
        events = self._set_events(name, instance)
        self._bind_events(events, instance.__dict__[name])

    def _bind_events(self, events, container):
        for event_name, event in events.items():
            setattr(container, event_name, event)
        return container

    def _set_events(self, name, instance):
        on = EventSlot()
        before = OverrideArgs()
        after = OverrideResult()
        def method(*args, **kwargs):
            args, kwargs = before(instance, *args, **kwargs)
            on(*args, **kwargs)
            result = self.__func__(*args, **kwargs)
            return after(result)
        instance.__dict__[name] = method
        return {'on': on, 'after': after, 'before': before}

    def _is_not_bound(self, instance):
        return self.func_name not in instance.__dict__


    def _assert_callable(self, func):
        if not callable(func):
            raise AttributeError('"%s" is not callable' % func)
