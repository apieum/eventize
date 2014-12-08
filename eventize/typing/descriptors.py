# -*- coding: utf8 -*-
from .events import AbstractHandler

Undefined = type('Undefined', (object, ), {})

class AbstractValue(object):
    """Encapsulate attribute value"""
    def get(self, default=Undefined):
        """return self.data"""
        raise NotImplemented()

    def set(self, value):
        """set self.data"""
        raise NotImplemented()

    def delete(self):
        """del attribute self.data"""
        raise NotImplemented()


class AbstractDescriptor(object):
    def __get__(self, instance, ownerCls=None):
        """If called at class return self else self.get"""
        raise NotImplemented()

    def __set__(self, instance, value):
        """If called at class return self else self.set"""
        raise NotImplemented()

    def __delete__(self, instance):
        """If called at class return self else self.delete"""
        raise NotImplemented()

    def get_value(self, instance):
        """return <Value> instance.__dict__[alias]"""
        raise NotImplemented()

    def get(self, instance):
        """return self.get_value(instance).get"""
        raise NotImplemented()

    def set(self, instance, value):
        """self.get_value(instance).set"""
        raise NotImplemented()

    def delete(self, instance):
        """self.get_value(instance).delete"""
        raise NotImplemented()

class HandlerDescriptor(AbstractDescriptor, AbstractHandler):
    "Methods or Attributes handlers"

class MethodDescriptor(HandlerDescriptor):
    "Methods handlers"

class AttributeDescriptor(HandlerDescriptor):
    "Attributes handlers"

