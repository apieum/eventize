# -*- coding: utf8 -*-
from events import EventSlot

class Attribute(object):
    __alias__ = None
    def __init__(self, default=None):
        self.on_get = EventSlot()
        self.on_set = EventSlot()
        self.on_del = EventSlot()
        self.default = default

    def __get__(self, instance, ownerCls):
        if instance is None:
            return self
        alias = self._get_alias(instance)
        self.on_get(instance, alias)
        try:
            self._assert_is_set(instance, alias)
        except AttributeError as error:
            if self.default is None:
                raise error
            self.__set__(instance, self.default)

        return instance.__dict__[alias]

    def __set__(self, instance, value):
        alias = self._get_alias(instance)
        self.on_set(instance, alias, value)
        instance.__dict__[alias] = self._set_events(instance, alias, value)

    def __delete__(self, instance):
        alias = self._get_alias(instance)
        self.on_del(instance, alias)
        if alias in instance.__dict__:
            del instance.__dict__[alias]

    def _find_alias(self, ownerCls):
        for attr, value in ownerCls.__dict__.iteritems():
            if value is self:
                return attr


    def _get_alias(self, instance):
        ownerCls = instance.__class__
        if self.__alias__ is None:
            self.__alias__ = self._find_alias(ownerCls)
        return self.__alias__

    def _assert_is_set(self, instance, attr):
        if attr not in instance.__dict__:
            raise AttributeError("AttributeError: '%s' has no attribute '%s'" % (instance, attr))

    def _set_events(self, instance, alias, value):
        try:
            setattr(value, 'on_get', self.on_get.called_with(instance))
            setattr(value, 'on_set', self.on_set.called_with(instance))
            setattr(value, 'on_del', self.on_del.called_with(instance))
        except AttributeError:
            value_type = type(value)
            bases = (value_type, ) + value_type.__bases__
            attrs = dict(value_type.__dict__)
            attrs['on_get'] = self.on_get.called_with(instance)
            attrs['on_set'] = self.on_set.called_with(instance)
            attrs['on_del'] = self.on_del.called_with(instance)

            EventValue = type(value_type.__name__, bases, attrs)
            value = EventValue(value)

        return value
