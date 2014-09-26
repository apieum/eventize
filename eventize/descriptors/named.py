# -*- coding: utf8 -*-
from .value import Value
from ..typing import AbstractDescriptor, Modifiable
from ..modifiers.descriptors import Default

class Named(AbstractDescriptor, Modifiable):
    __alias__ = None
    default = None
    ValueType = Value

    def __init__(self, *args, **kwargs):
        for item, value in tuple(kwargs.items()):
            setattr(self, item, value)
        self.accept_all(*args)

    def reject(self, arg):
        self.accept(Default(arg))

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

    def __get__(self, instance, ownerCls=None):
        if instance is None: return self
        return self.get(instance)

    def __set__(self, instance, value):
        if instance is None: return self
        self.set(instance, value)

    def __delete__(self, instance):
        if instance is None: return self
        self.delete(instance)

    def is_set(self, instance, alias):
        return alias in instance.__dict__

    def get(self, instance):
        return self.get_value(instance).get()

    def set(self, instance, value):
        self.get_value(instance).set(value)

    def delete(self, instance):
        self.get_value(instance).delete()

