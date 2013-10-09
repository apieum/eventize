# -*- coding: utf8 -*-
from .method import Method as EventedMethod
from .attribute import Attribute as EventedAttribute

__all__ = ['Observable', 'EventedMethod', 'EventedAttribute']

def Observable(cls):
    for attr, value in list(cls.__dict__.items()):
        if attr[0] == '_': continue
        if is_a_method(value):
            setattr(cls, attr, EventedMethod(value))
        else:
            setattr(cls, attr, EventedAttribute(value))
    return cls

def is_a_method(method):
    from types import BuiltinFunctionType, BuiltinMethodType, FunctionType, LambdaType, MethodType
    return isinstance(method, (BuiltinFunctionType, BuiltinMethodType, FunctionType, LambdaType, MethodType))

