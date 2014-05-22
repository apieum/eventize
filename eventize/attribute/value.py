# -*- coding: utf8 -*-
from .handler import InstanceHandler
from .event import OnGetEvent, OnSetEvent, OnDelEvent, OnChangeEvent
from ..descriptors import value

class Value(value.Value):
    def set_handlers(self):
        self.on_get = InstanceHandler()
        self.on_set = InstanceHandler()
        self.on_del = InstanceHandler()
        self.on_change = InstanceHandler()


    def get(self):
        event = OnGetEvent(self)
        self.notify('on_get', event)
        return event.returns()

    def set(self, value):
        event = OnSetEvent(self, value=value)
        self.notify('on_set', event)
        if self.has_changed(event.returns()):
            event = OnChangeEvent(event)
            self.notify('on_change', event)
        setattr(self, 'data', event.returns())

    def delete(self):
        event = OnDelEvent(self)
        self.notify('on_del', event)
        delattr(self, 'data')

    def has_changed(self, value):
        return not hasattr(self, 'data') or value != self.data

