# -*- coding: utf8 -*-
from .events import EventSlot, Event

class Attribute(object):
    __alias__ = None
    def __init__(self, default=None):
        self._set_events(self)
        self.default = default

    def __get__(self, instance, ownerCls):
        if instance is None:
            return self
        alias = self._get_alias(instance)

        event = Event(instance, alias=alias)
        self.on_get(event)
        try:
            self._assert_is_set(event.instance, event.alias)
        except AttributeError as error:
            if self.default is None:
                raise error
            self.__set__(event.instance, self.default)

        event.instance.__dict__[event.alias].on_get(event)
        return event.instance.__dict__[event.alias]

    def __set__(self, instance, value):
        alias = self._get_alias(instance)
        event = Event(instance, alias=alias, value=value)
        self.on_set(event)
        if alias in instance.__dict__:
            instance.__dict__[alias].on_set(event)
        instance.__dict__[alias] = self._set_events(event.value)

    def __delete__(self, instance):
        alias = self._get_alias(instance)
        event = Event(instance, alias=alias)
        self.on_del(event)
        if alias in event.instance.__dict__:
            event.instance.__dict__[alias].on_del(event)
            del event.instance.__dict__[alias]

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
            raise AttributeError("'%s' has no attribute '%s'" % (instance, attr))


    def _set_events(self, instance, copy_from=None):
        on_get = getattr(copy_from, 'on_get', EventSlot())
        on_set = getattr(copy_from, 'on_set', EventSlot())
        on_del = getattr(copy_from, 'on_del', EventSlot())
        try:
            setattr(instance, 'on_get', on_get)
            setattr(instance, 'on_set', on_set)
            setattr(instance, 'on_del', on_del)
        except AttributeError:
            instance_type = type(instance)
            bases = (instance_type, ) + instance_type.__bases__
            attrs = dict(instance_type.__dict__)
            attrs['on_get'] = on_get
            attrs['on_set'] = on_set
            attrs['on_del'] = on_del

            EventValue = type(instance_type.__name__, bases, attrs)
            instance = EventValue(instance)

        return instance
