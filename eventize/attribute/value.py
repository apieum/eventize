# -*- coding: utf8 -*-
from .handler import InstanceHandler
from .event import OnGetEvent, OnSetEvent, OnDelEvent, OnChangeEvent
from ..descriptors import value

class Value(value.Value):
    event_types = {
        'on_get':OnGetEvent,
        'on_set':OnSetEvent,
        'on_del':OnDelEvent,
        'on_change':OnChangeEvent
    }
    def set_handlers(self):
        self.on_get = InstanceHandler()
        self.on_set = InstanceHandler()
        self.on_del = InstanceHandler()
        self.on_change = InstanceHandler()


    def get(self):
        return self.notify('on_get', self).returns()

    def set(self, value):
        event = self.notify('on_set', self, value=value)
        if self.has_changed(event.returns()):
            event = self.notify('on_change', event)
        setattr(self, 'data', event.returns())

    def delete(self):
        self.notify('on_del', self)
        delattr(self, 'data')

    def has_changed(self, value):
        return not hasattr(self, 'data') or value != self.data

