# -*- coding: utf8 -*-
from types import BuiltinFunctionType, BuiltinMethodType, FunctionType, LambdaType, MethodType
from .descriptors import *

methods = (MethodDescriptor, BuiltinFunctionType, BuiltinMethodType, FunctionType, LambdaType, MethodType)
is_a_method = lambda method: isinstance(method, methods)

def resolve_type(cls_field, handler_type=None):
    if handler_type is not None: return handler_type
    if is_a_method(cls_field):
        from eventize.method import Method
        return Method
    from eventize.attribute import Attribute
    return Attribute
