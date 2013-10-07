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

        try:
            self._assert_is_set(instance, alias)
        except AttributeError as error:
            if self.default is None:
                raise error
            self.__set__(instance, self.default)

        event = Event(instance, alias=alias, value=instance.__dict__[alias])
        self.trigger_event(instance.__dict__[alias], 'on_get', event)
        return event.instance.__dict__[event.alias]

    def __set__(self, instance, value):
        alias = self._get_alias(instance)
        event = Event(instance, alias=alias, value=value)
        if alias in instance.__dict__:
            self.trigger_event(instance.__dict__[alias], 'on_set', event)
        else:
            self.on_set(event)
        instance.__dict__[alias] = self._set_events(event.value)

    def __delete__(self, instance):
        alias = self._get_alias(instance)
        if alias in instance.__dict__:
            event = Event(instance, alias=alias, value=instance.__dict__[alias])
            self.trigger_event(instance.__dict__[alias], 'on_del', event)
            del event.instance.__dict__[alias]

    def trigger_event(self, instance, event_name, event):
        getattr(self, event_name)(event)
        callback = getattr(instance, event_name, lambda event:None)
        return callback(event)

    def clean(self):
        self.on_get.remove_all()
        self.on_set.remove_all()
        self.on_del.remove_all()

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
        event_get = getattr(copy_from, 'on_get', EventSlot())
        event_set = getattr(copy_from, 'on_set', EventSlot())
        event_del = getattr(copy_from, 'on_del', EventSlot())
        try:
            setattr(instance, 'on_get', event_get)
            setattr(instance, 'on_set', event_set)
            setattr(instance, 'on_del', event_del)
        except AttributeError:
            instance_type = type(instance)
            bases = instance_type.__bases__
            attrs = dict(instance_type.__dict__)
            attrs['on_get'] = event_get
            attrs['on_set'] = event_set
            attrs['on_del'] = event_del
            try:
                EventValue = type(instance_type.__name__, (instance_type, ) + bases, attrs)
                instance = EventValue(instance)
            except TypeError:
                pass

        return instance
