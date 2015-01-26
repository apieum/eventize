# -*- coding: utf8 -*-
from .events import AbstractHandler

Undefined = type('Undefined', (object, ), {})

class AbstractValue(object):
    """Encapsulate attribute value"""
    def get(self, default=Undefined):
        """return self.data"""
        raise NotImplementedError("AbstractValue.get must be overriden")

    def set(self, value):
        """set self.data"""
        raise NotImplementedError("AbstractValue.set must be overriden")

    def delete(self):
        """del attribute self.data"""
        raise NotImplementedError("AbstractValue.delete must be overriden")


class AbstractDescriptor(object):
    def __get__(self, instance, ownerCls=None):
        """If called at class level return self else self.get"""
        if instance is None: return self
        return self.get(instance)

    def __set__(self, instance, value):
        """If called at class level return self else self.set"""
        if instance is None: return self
        self.set(instance, value)

    def __delete__(self, instance):
        """If called at class level return self else self.delete"""
        if instance is None: return self
        self.delete(instance)


    def get(self, instance, default=Undefined):
        """return self.get_value(instance).get"""
        return self.get_value(instance).get(default)

    def set(self, instance, value):
        """self.get_value(instance).set"""
        self.get_value(instance).set(value)

    def delete(self, instance):
        """self.get_value(instance).delete"""
        self.get_value(instance).delete()

    def get_value(self, instance):
        """return <Value> instance.__dict__[alias]"""
        raise NotImplementedError("AbstractDescriptor.get_value must be overriden")


class MethodDescriptor:
    "Methods handlers"

class AttributeDescriptor:
    "Attributes handlers"

