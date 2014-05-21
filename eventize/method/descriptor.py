# -*- coding: utf8 -*-
from .. import descriptors
from .handler import Handler, Subject, InstanceHandler


class Value(object):
    def __init__(self, value, instance, alias):
        cls = getattr(type(instance), alias)
        desc = type(cls)
        self.before = InstanceHandler()
        self.after = InstanceHandler()

        def func(*args, **kwargs):
            event = desc.before.trigger(instance, *args, **kwargs)
            cls.before(event)
            self.before(event)
            event.call(self.__func__)
            desc.after(event)
            cls.after(event)
            self.after(event)
            return event.returns()

        self.name = alias
        setattr(func, '__name__', self.name)
        setattr(self, self.name, func)
        if value is not None:
            self.set(value)

    def get(self):
        return getattr(self, self.name)

    def set(self, value):
        self._assert_callable(value)
        self.__func__ = value
        setattr(self.get(), '__func__', value)

    def delete(self):
        delattr(self, self.name)

    def _assert_callable(self, func):
        if not callable(func):
            raise AttributeError('"%s" is not callable' % func)


@Subject
class Descriptor(descriptors.Named):
    ValueType = Value
    before = Handler()
    after = Handler()

    def before_instance(self, instance):
        return self.get_value(instance).before

    def after_instance(self, instance):
        return self.get_value(instance).after


