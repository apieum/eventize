# -*- coding: utf8 -*-
from .. import descriptors
from .handler import Handler, Subject, InstanceHandler
from .event import Event

class Value(descriptors.Value):
    def set_handlers(self):
        self.on_get = InstanceHandler()
        self.on_set = InstanceHandler()
        self.on_del = InstanceHandler()
        self.on_change = InstanceHandler()


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


@Subject
class Descriptor(descriptors.Named):
    ValueType = Value
    on_get = Handler()
    on_set = Handler()
    on_del = Handler()
    on_change = Handler()
