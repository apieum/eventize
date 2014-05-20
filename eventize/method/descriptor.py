# -*- coding: utf8 -*-
from .. import descriptors
from .handler import Handler, Subject, InstanceHandler

@Subject
class Descriptor(descriptors.Named):
    before = Handler()
    after = Handler()

    def before_instance(self, instance):
        return self.get_value(instance).before

    def after_instance(self, instance):
        return self.get_value(instance).after

    def get_value(self, instance, default=None):
        return self.get(instance, self.get_alias(instance), default)

    def set_args(self, instance, name, func):
        value = self.get(instance, name, MethodInstance(instance, self, func))
        return instance, name, value.update(func)


class MethodInstance(object):
    def __init__(self, instance, parent, func):
        self.instance = instance
        self.parent = parent
        self.update(func).__name__ = parent.get_alias(instance)
        self.before = InstanceHandler()
        self.after = InstanceHandler()

    def update(self, func):
        self._assert_callable(func)
        self.__func__ = func
        return self

    def _assert_callable(self, func):
        if not callable(func):
            raise AttributeError('"%s" is not callable' % func)

    def __call__(self, *args, **kwargs):
        event = self.parent.before.trigger(self.instance, *args, **kwargs)
        self.before(event)
        event.call(self.__func__)
        self.parent.after(event)
        self.after(event)
        return event.returns()
