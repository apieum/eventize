# -*- coding: utf8 -*-
from .value import Value
from ..typing import AbstractDescriptor, Modifiable
from ..modifiers.descriptors import Default

class Named(AbstractDescriptor, Modifiable):
    __alias__ = None
    ValueType = Value

    def __init__(self, *args, **kwargs):
        Modifiable.__init__(self)
        for item, value in tuple(kwargs.items()):
            setattr(self, item, value)
        self.accept_all(*args)

    @property
    def default(self):
        return self.__dict__.get('default', None)

    @default.setter
    def default(self, value):
        self.accept(Default(value))

    def reject(self, arg):
        self.default = arg

    def defer(self, modifier):
        self.remove_visitor(modifier)

    def find_alias(self, ownerCls):
        for attr, value in list(ownerCls.__dict__.items()):
            if value is self: return attr

    def get_alias(self, instance):
        if self.__alias__ is None:
            self.__alias__ = self.find_alias(type(instance))
        return self.__alias__

    def get_value(self, instance):
        alias = self.get_alias(instance)
        self.set_value_once(instance, alias)
        return instance.__dict__[alias]

    def set_value_once(self, instance, alias):
        if self.is_set(instance, alias): return
        default = getattr(self, 'default', None)
        instance.__dict__[alias] = self.ValueType(instance, alias, default)

    def is_set(self, instance, alias):
        return alias in instance.__dict__


