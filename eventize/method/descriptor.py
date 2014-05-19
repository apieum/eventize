# -*- coding: utf8 -*-
from .. import descriptors
from .handler import Handler, Subject

@Subject
class Descriptor(descriptors.Named):
    before = Handler()
    after = Handler()

    def set_args(self, instance, name, func):
        value = self.get(instance, name, MethodInstance(instance, self, func))
        return instance, name, value.update(func)


class MethodInstance(object):
    def __init__(self, instance, parent, func):
        self.instance = instance
        self.update(func).__name__ = parent.get_alias(instance)
        self.before = type(parent).before.build_instance_handler(parent)
        self.after = type(parent).after.build_instance_handler(parent)

    def update(self, func):
        self._assert_callable(func)
        self.__func__ = func
        return self

    def _assert_callable(self, func):
        if not callable(func):
            raise AttributeError('"%s" is not callable' % func)

    def __call__(self, *args, **kwargs):
        event = self.before.trigger(self.instance, *args, **kwargs)
        event.call(self.__func__)
        self.after(event)
        return event.returns()
