# -*- coding: utf8 -*-

class Named(object):
    __alias__ = None

    def __init__(self, default=None):
        self.default = default

    def find_alias(self, ownerCls):
        for attr, value in ownerCls.__dict__.items():
            if value is self:
                return attr

    def get_alias(self, instance):
        if self.__alias__ is None:
            self.__alias__ = self.find_alias(type(instance))
        return self.__alias__


    def __get__(self, instance, ownerCls):
        if instance is None: return self
        alias = self.get_alias(instance)
        if self.is_not_set(instance, alias):
            self.set_default(instance, alias)
        value = self.get(instance, alias)
        return self.get_result(instance, alias, value)

    def __set__(self, instance, value):
        if instance is None: return self
        alias = self.get_alias(instance)
        args = self.set_args(instance, alias, value)
        self.set(*args)

    def __delete__(self, instance):
        if instance is None: return self
        alias = self.get_alias(instance)
        if self.is_set(instance, alias):
            self.delete(instance, alias)

    def is_set(self, instance, alias):
        return alias in instance.__dict__

    def is_not_set(self, instance, alias):
        return not self.is_set(instance, alias)

    def get(self, instance, alias, default=None):
        if self.is_set(instance, alias):
            default = instance.__dict__[alias]
        return default

    def set(self, instance, alias, value):
        instance.__dict__[alias] = value

    def delete(self, instance, alias):
        del instance.__dict__[alias]

    def set_args(self, instance, alias, value):
        return instance, alias, value

    def get_result(self, instance, alias, value):
        return value


    def set_default(self, instance, alias):
        if self.default is None:
            raise AttributeError("'%s' has no attribute '%s'" % (instance, alias))
        setattr(instance, alias, self.default)
