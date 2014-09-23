# -*- coding: utf8 -*-
from ..typing import Undefined
from ..descriptors import handlerValue
from .handler import OnGet, OnSet, OnDel, OnChange


class Value(handlerValue.Value):
    def set_handlers(self):
        self.on_get = OnGet()
        self.on_set = OnSet()
        self.on_del = OnDel()
        self.on_change = OnChange()

    def get(self, default=Undefined):
        return self.notify('on_get', self, value=super(Value, self).get(default)).returns()

    def set(self, value):
        value = self.notify('on_set', self, value=value).returns()
        if self.has_changed(value):
            parent = super(Value, self)
            old_value = parent.get(None)
            parent.set(value)
            value = self.notify('on_change', self, value=value, old_value=old_value).returns()
            parent.set(value)

    def delete(self):
        self.notify('on_del', self)
        super(Value, self).delete()

