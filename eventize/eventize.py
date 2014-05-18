# -*- coding: utf8 -*-
from .method.descriptor import Method
from .attribute.descriptor import Attribute
from types import BuiltinFunctionType, BuiltinMethodType, FunctionType, LambdaType, MethodType

__all__ = ['Observable', 'Observer', 'handle']


def Observable(cls):
    fields = filter(lambda attr: not attr[0].startswith('_'), cls.__dict__.items())
    for attr, value in fields:
        setattr(cls, attr, Observer(value))
    return cls

def Observer(value):
    if is_a_method(value):
        return Method(value)
    return Attribute(value)

methods = (BuiltinFunctionType, BuiltinMethodType, FunctionType, LambdaType, MethodType)
is_a_method = lambda method: isinstance(method, methods)

def handle(obj, name):
    cls = isinstance(obj, type) and obj or type(obj)
    if not isinstance(getattr(cls, name), Method):
        setattr(cls, name, Method(getattr(cls, name)))
    return getattr(obj, name)
