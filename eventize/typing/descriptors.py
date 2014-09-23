# -*- coding: utf8 -*-
from .abstract import base_class

@base_class
class HandlerDescriptor(object):
    "Methods or Attributes handlers"

@base_class
class MethodDescriptor(HandlerDescriptor):
    "Methods handlers"

@base_class
class AttributeDescriptor(HandlerDescriptor):
    "Attributes handlers"

