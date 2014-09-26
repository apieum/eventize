# -*- coding: utf8 -*-
from .descriptors import *
from .events import *
from .modifiers import *

def is_a_method(method):
    from types import BuiltinFunctionType, BuiltinMethodType, FunctionType, LambdaType, MethodType
    return isinstance(method, (MethodDescriptor, BuiltinFunctionType, BuiltinMethodType, FunctionType, LambdaType, MethodType))


def resolve_type(cls_field):
    if is_a_method(cls_field):
        from eventize.method import Method
        return Method
    from eventize.attribute import Attribute
    return Attribute
