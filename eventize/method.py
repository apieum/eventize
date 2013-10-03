# -*- coding: utf8 -*-
from events import OverrideArgs, OverrideResult, EventSlot


class Method(object):
    def __init__(self, func):
        self.__assert_callable(func)

        self.func_name = getattr(func, 'func_name', 'method')
        self.func_doc = getattr(func, 'func_doc', '')
        self.__func__ = func

        events = self.__set_events('__call__', self)
        for event_name, event in events.items():
            setattr(self, event_name, event)

    def __call__(self, *args, **kwargs):
        return self.__dict__['__call__'](*args, **kwargs)

    def __get__(self, instance, ownerCls):
        if instance is None: return self

        if self.__is_not_bound(instance):
            self.__bind_method(self.func_name, instance)

        return instance.__dict__[self.func_name]

    def __bind_method(self, name, instance):
        events = self.__set_events(name, instance)
        for event_name, event in events.items():
            setattr(instance.__dict__[name], event_name, event)


    def __set_events(self, name, instance):
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

    def __is_not_bound(self, instance):
        return self.func_name not in instance.__dict__


    def __assert_callable(self, func):
        if not callable(func):
            raise AttributeError('"%s" is not callable' % func)
