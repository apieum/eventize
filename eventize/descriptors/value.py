# -*- coding: utf8 -*-
from ..typing import Undefined, AbstractValue

class Value(AbstractValue):
    def __init__(self, instance, alias, value):
        self.instance = instance
        self.ownerCls = getattr(type(instance), alias, None)
        self.name = alias
        self.init_value(value)

    def init_value(self, value):
        self.set(value)

    def get(self, default=Undefined):
        result = getattr(self, 'data', default)
        if result is Undefined:
            raise AttributeError("%s has no attribute '%s'" % (self.instance, self.name))
        return result

    def set(self, value):
        if self.has_changed(value):
            setattr(self, 'data', value)

    def delete(self):
        delattr(self, 'data')

    def has_changed(self, value):
        return value is not getattr(self, 'data', None)
