# -*- coding: utf8 -*-
from .value import Value
from ..typing import AbstractDescriptor, Modifiers
from ..modifiers.descriptors import Default

class NamedModifiers(Modifiers):

    def refuse(self, visited, visitor):
        self.append(visited, Default(visitor))

    def reject(self, visited, visitor):
        self.remove(visitor)


class Named(AbstractDescriptor):
    __alias__ = None
    ValueType = Value

    def __init__(self, *args, **kwargs):
        self.visitors = NamedModifiers(args)
        if "default" in kwargs:
            self.visitors.push(Default(kwargs.get("default")))
        self.visitors.visit(self)

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


