# -*- coding: utf8 -*-
from .events import EventSlot, Event
from .namedDescriptor import NamedDescriptor

class Attribute(NamedDescriptor):
    def __init__(self, default=None):
        self._set_events(self)
        self.default = default

    def __get__(self, instance, ownerCls):
        if instance is None:
            return self
        name = self._get_name(instance)
        self._assert_is_set(instance, name)

        event = self.make_event(instance, name, instance.__dict__[name])
        self.trigger_event(instance.__dict__[name], 'on_get', event)
        return event.instance.__dict__[event.name]

    def __set__(self, instance, value):
        name = self._get_name(instance)
        event = self.make_event(instance, name, value)
        if name in instance.__dict__:
            self.trigger_event(instance.__dict__[name], 'on_set', event)
        else:
            self.on_set(event)
        instance.__dict__[name] = self._set_events(event.value)

    def __delete__(self, instance):
        name = self._get_name(instance)
        if name in instance.__dict__:
            event = self.make_event(instance, name, instance.__dict__[name])
            self.trigger_event(instance.__dict__[name], 'on_del', event)
            del event.instance.__dict__[name]

    def make_event(self, instance, name, value):
        return Event(instance, name=name, value=value)

    def trigger_event(self, instance, event_name, event):
        getattr(self, event_name)(event)
        callback = getattr(instance, event_name, lambda event:None)
        return callback(event)

    def clean(self):
        self.on_get.remove_all()
        self.on_set.remove_all()
        self.on_del.remove_all()

    def _assert_is_set(self, instance, name):
        if name not in instance.__dict__:
            if self.default is None:
                raise AttributeError("'%s' has no attribute '%s'" % (instance, name))
            self.__set__(instance, self.default)


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
