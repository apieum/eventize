# -*- coding: utf8 -*-
from .namedDescriptor import NamedDescriptor
from .events.handler import MethodHandler, InstanceHandler
from .events.subject import Subject

__all__ = ['Method']

@Subject
class Method(NamedDescriptor):
    before = MethodHandler()
    after = MethodHandler()

    def __init__(self, func):
        self._assert_callable(func)
        self.__func__ = func

    def get(self, instance, name):
        if self.is_not_set(instance, name):
            self.set(instance, name, self)
        return instance.__dict__[name]

    def set(self, instance, name, func):
        instance.__dict__[name] = InstanceMethod(instance, name, func)

    def _assert_callable(self, func):
        if not callable(func):
            raise AttributeError('"%s" is not callable' % func)


class InstanceMethod(object):
    def __init__(self, instance, name, parent):
        self.instance = instance
        self.parent = parent
        self.__name__ = name
        self.before = InstanceHandler()
        self.before.parent = type(parent).before
        self.before.parentInstance = parent.before
        self.after = InstanceHandler()
        self.after.parent = type(parent).after
        self.after.parentInstance = parent.after

    def __call__(self, *args, **kwargs):
        event = self.before.call(self.instance, *args, **kwargs)
        event.call(self.parent.__func__)
        self.after(event)
        return event.returns()
