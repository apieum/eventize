# -*- coding: utf8 -*-
from .method.descriptor import Method as ObservedMethod
from .attribute.descriptor import Attribute as ObservedAttribute
from types import BuiltinFunctionType, BuiltinMethodType, FunctionType, LambdaType, MethodType

__all__ = ['Observable', 'ObservedMethod', 'ObservedAttribute', 'Observer']


def Observable(cls):
    fields = filter(lambda attr: not attr[0].startswith('_'), cls.__dict__.items())
    for attr, value in fields:
        setattr(cls, attr, Observer(value))
    return cls

def Observer(value):
    if is_a_method(value):
        return ObservedMethod(value)
    return ObservedAttribute(value)


def is_a_method(method):
    return isinstance(
        method,
        (BuiltinFunctionType, BuiltinMethodType, FunctionType, LambdaType, MethodType)
    )

