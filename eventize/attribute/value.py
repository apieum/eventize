# -*- coding: utf8 -*-
from .handler import InstanceHandler
from .event import Event
from ..descriptors import value

class Value(value.Value):
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

