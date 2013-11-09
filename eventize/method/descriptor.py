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

    def set_default(self, instance, name):
        self.set(instance, name, self.__func__)

    def set(self, instance, name, func):
        if self.is_set(instance, name):
            self.get(instance, name).update(func)
        else:
            super(Method, self).set(instance, name, MethodInstance(instance, self, func))

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

    def update(self, func):
        self.__func__ = func

    def __call__(self, *args, **kwargs):
        event = self.before.call(self.instance, *args, **kwargs)
        event.call(self.__func__)
        self.after(event)
        return event.returns()
