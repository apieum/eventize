# -*- coding: utf8 -*-
from .wrappers import WrapCondition

class Value(object):
    def __init__(self, value, instance, alias):
        self.instance = instance
        self.ownerCls = getattr(type(instance), alias, None)
        self.name = alias
        self.init_value(value)

    def init_value(self, value):
        if value is not None:
            self.set(value)

    def get(self):
        return self.data

    def set(self, value):
        self.data = value

    def delete(self):
        delattr(self, 'data')
