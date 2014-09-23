# -*- coding: utf8 -*-
from types import BuiltinFunctionType, BuiltinMethodType, FunctionType, LambdaType, MethodType
from ..method import Method
from ..attribute import Attribute

__all__ = ['Attribute', 'Method', 'is_a_method']

methods = (Method, BuiltinFunctionType, BuiltinMethodType, FunctionType, LambdaType, MethodType)
is_a_method = lambda method: isinstance(method, methods)

def resolve_type(cls_field, handler_type=None):
    if handler_type is not None: return handler_type
    return is_a_method(cls_field) and Method or Attribute

