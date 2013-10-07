# -*- coding: utf8 -*-
from .method import Method as EventMethod
from .attribute import Attribute as EventAttribute

__all__ = ['Observable', 'EventMethod', 'EventAttribute']

def Observable(cls):
    for attr, value in list(cls.__dict__.items()):
        if attr[0] == '_': continue
        if is_a_method(value):
            setattr(cls, attr, EventMethod(value))
        else:
            setattr(cls, attr, EventAttribute(value))
    return cls

def is_a_method(method):
    from types import BuiltinFunctionType, BuiltinMethodType, FunctionType, LambdaType, MethodType
    return isinstance(method, (BuiltinFunctionType, BuiltinMethodType, FunctionType, LambdaType, MethodType))

