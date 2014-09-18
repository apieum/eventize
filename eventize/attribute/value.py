# -*- coding: utf8 -*-
from ..descriptors import handlerValue
from .handler import OnGet, OnSet, OnDel, OnChange

class Value(handlerValue.Value):
    def set_handlers(self):
        self.on_get = OnGet()
        self.on_set = OnSet()
        self.on_del = OnDel()
        self.on_change = OnChange()

    def get(self):
        return self.notify('on_get', self).returns()

    def set(self, value):
        value = self.notify('on_set', self, value=value).returns()
        if self.has_changed(value):
            setattr(self, 'data', value)
            value = self.notify('on_change', self, value=value).returns()
            if self.has_changed(value):
                setattr(self, 'data', value)

    def delete(self):
        self.notify('on_del', self)
        delattr(self, 'data')

    def has_changed(self, value):
        return not hasattr(self, 'data') or value is not self.data

