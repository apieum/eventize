# -*- coding: utf8 -*-

class NamedDescriptor(object):
    __name__ = None
    def find_name(self, ownerCls):
        for attr, value in ownerCls.__dict__.items():
            if value is self:
                return attr

    def get_name(self, instance):
        if self.__name__ is None:
            self.__name__ = self.find_name(type(instance))
        return self.__name__


    def __get__(self, instance, ownerCls):
        if instance is None: return self
        name = self.get_name(instance)
        return self.get(instance, name)

    def __set__(self, instance, value):
        if instance is None: return self
        name = self.get_name(instance)
        return self.set(instance, name, value)

    def __delete__(self, instance):
        if instance is None: return self
        name = self.get_name(instance)
        if self.is_set(instance, name):
            self.delete(instance, name)

    def is_set(self, instance, name):
        return name in instance.__dict__

    def get(self, instance, name):
        raise NotImplementedError("%s.get must be implemented" % type(self).__name__)

    def set(self, instance, name, value):
        raise NotImplementedError("%s.set must be implemented" % type(self).__name__)

    def delete(self, instance, name):
        raise NotImplementedError("%s.delete must be implemented" % type(self).__name__)
