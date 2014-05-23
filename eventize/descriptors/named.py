# -*- coding: utf8 -*-
from .value import Value

class Named(object):
    __alias__ = None
    ValueType = Value

    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        list(map(self.visit, args))

        if 'default' in self.kwargs:
            self.default = self.kwargs['default']

        delattr(self, 'args')
        delattr(self, 'kwargs')

    def visit(self, arg):
        visit = getattr(arg, 'visit', lambda obj: setattr(obj, 'default', arg))
        return visit(self)

    def find_alias(self, ownerCls):
        for attr, value in list(ownerCls.__dict__.items()):
            if value is self: return attr

    def get_alias(self, instance):
        if self.__alias__ is None:
            self.__alias__ = self.find_alias(type(instance))
        return self.__alias__

    def get_value(self, instance):
        alias = self.get_alias(instance)
        self.set_default(instance, alias)
        return self.get(instance, alias)

    def __get__(self, instance, ownerCls=None):
        if instance is None: return self
        return self.get_value(instance).get()

    def __set__(self, instance, value):
        if instance is None: return self
        alias = self.get_alias(instance)
        self.set(instance, alias, value)

    def __delete__(self, instance):
        if instance is None: return self
        alias = self.get_alias(instance)
        if self.is_set(instance, alias):
            self.delete(instance, alias)

    def is_set(self, instance, alias):
        return alias in instance.__dict__

    def is_not_set(self, instance, alias):
        return not self.is_set(instance, alias)

    def get(self, instance, alias):
        return instance.__dict__[alias]

    def set(self, instance, alias, value):
        if self.is_set(instance, alias):
            instance.__dict__[alias].set(value)
        else:
            instance.__dict__[alias] = self.ValueType(value, instance, alias)

    def delete(self, instance, alias):
        instance.__dict__[alias].delete()

    def set_default(self, instance, alias):
        if self.is_set(instance, alias): return True
        default = getattr(self, 'default', None)
        setattr(instance, alias, default)
        return default != None


