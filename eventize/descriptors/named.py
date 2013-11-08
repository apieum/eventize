# -*- coding: utf8 -*-

class Named(object):
    __alias__ = None
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
        return self.get(instance, alias)

    def __set__(self, instance, value):
        if instance is None: return self
        alias = self.get_alias(instance)
        return self.set(instance, alias, value)

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
        raise self.__method_not_implemented('get')

    def set(self, instance, alias, value):
        raise self.__method_not_implemented('set')

    def delete(self, instance, alias):
        raise self.__method_not_implemented('delete')

    def __method_not_implemented(self, method_name):
        message = "%s.%s must be implemented" %(type(self).__name__, method_name)
        return NotImplementedError(message)
