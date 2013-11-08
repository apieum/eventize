# -*- coding: utf8 -*-
from ..descriptors import NamedDescriptor
from .handler import MethodHandler, MethodSubject

__all__ = ['Method']

@MethodSubject
class Method(NamedDescriptor):
    before = MethodHandler()
    after = MethodHandler()

    def __init__(self, func):
        self._assert_callable(func)
        self.__func__ = func

    def get(self, instance, name):
        if self.is_not_set(instance, name):
            self.set(instance, name, self.__func__)
        return instance.__dict__[name]

    def set(self, instance, name, func):
        if self.is_set(instance, name):
            method_instance = getattr(instance, name)
            method_instance.__func__ = func
        else:
            method_instance = MethodInstance(instance, self, func)
        instance.__dict__[name] = method_instance

    def _assert_callable(self, func):
        if not callable(func):
            raise AttributeError('"%s" is not callable' % func)


class MethodInstance(object):
    def __init__(self, instance, parent, func):
        self.instance = instance
        self.__name__ = parent.get_alias(instance)
        self.__func__ = func
        self.before = type(parent).before.build_instance_handler(parent)
        self.after = type(parent).after.build_instance_handler(parent)

    def __call__(self, *args, **kwargs):
        event = self.before.call(self.instance, *args, **kwargs)
        event.call(self.__func__)
        self.after(event)
        return event.returns()
