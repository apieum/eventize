# -*- coding: utf8 -*-
from .. import descriptors
from .handler import Handler, Subject, InstanceHandler
from .event import Event

class Value(object):
    def __init__(self, value, instance, alias):
        self.instance = instance
        self.name = alias
        self.cls = getattr(type(instance), alias)
        self.desc = type(self.cls)
        self.on_get = InstanceHandler()
        self.on_set = InstanceHandler()
        self.on_del = InstanceHandler()
        self.on_change = InstanceHandler()
        if value is not None:
            self.set(value)

    def get(self):
        event = Event(self.instance, name=self.name, value=self.data)
        self.notify('on_get', event)
        return event.returns()

    def set(self, value):
        event = Event(self.instance, name=self.name, value=value)
        self.notify('on_set', event)
        if self.has_changed(event.value):
            self.notify('on_change', event)
        setattr(self, 'data', event.returns())

    def delete(self):
        event = Event(self.instance, name=self.name, value=self.data)
        self.notify('on_del', event)
        delattr(self, 'data')

    def has_changed(self, value):
        return not hasattr(self, 'data') or value != self.data

    def notify(self, event_name, event):
        getattr(self.desc, event_name)(event)
        getattr(self.cls, event_name)(event)
        getattr(self, event_name)(event)
        return event


@Subject
class Descriptor(descriptors.Named):
    ValueType = Value
    on_get = Handler()
    on_set = Handler()
    on_del = Handler()
    on_change = Handler()
