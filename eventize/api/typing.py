# -*- coding: utf8 -*-
from types import BuiltinFunctionType, BuiltinMethodType, FunctionType, LambdaType, MethodType
from abc import ABCMeta

__all__ = ['is_a_method']


class HandlerDescriptor(object):
    pass

HandlerDescriptor = ABCMeta(str('HandlerDescriptor'), (HandlerDescriptor, ), {})

class MethodDescriptor(HandlerDescriptor):
    pass

MethodDescriptor = ABCMeta(str('MethodDescriptor'), (MethodDescriptor, ), {})

class AttributeDescriptor(HandlerDescriptor):
    pass

AttributeDescriptor = ABCMeta(str('AttributeDescriptor'), (AttributeDescriptor, ), {})

methods = (MethodDescriptor, BuiltinFunctionType, BuiltinMethodType, FunctionType, LambdaType, MethodType)
is_a_method = lambda method: isinstance(method, methods)

def resolve_type(cls_field, handler_type=None):
    from eventize.method import Method
    from eventize.attribute import Attribute
    if handler_type is not None: return handler_type
    return is_a_method(cls_field) and Method or Attribute
