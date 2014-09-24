# -*- coding: utf8 -*-
from .abstract import abstract, abstractmethod
from .events import AbstractHandler

Undefined = abstract(type('Undefined', (object, ), {}))

@abstract
class AbstractValue(object):
    """Encapsulate attribute value"""
    @abstractmethod
    def get(self, default=Undefined):
        """return self.data"""

    @abstractmethod
    def set(self, value):
        """set self.data"""

    @abstractmethod
    def delete(self):
        """del attribute self.data"""


@abstract
class AbstractDescriptor(object):
    @abstractmethod
    def __get__(self, instance, ownerCls=None):
        """If called at class return self else self.get"""

    @abstractmethod
    def __set__(self, instance, value):
        """If called at class return self else self.set"""

    @abstractmethod
    def __delete__(self, instance):
        """If called at class return self else self.delete"""

    @abstractmethod
    def get_value(self, instance):
        """return <Value> instance.__dict__[alias]"""

    @abstractmethod
    def get(self, instance):
        """return self.get_value(instance).get"""

    @abstractmethod
    def set(self, instance, value):
        """self.get_value(instance).set"""

    @abstractmethod
    def delete(self, instance):
        """self.get_value(instance).delete"""

@abstract
class HandlerDescriptor(AbstractDescriptor, AbstractHandler):
    "Methods or Attributes handlers"

@abstract
class MethodDescriptor(HandlerDescriptor):
    "Methods handlers"

@abstract
class AttributeDescriptor(HandlerDescriptor):
    "Attributes handlers"

