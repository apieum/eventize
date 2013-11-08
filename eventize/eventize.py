# -*- coding: utf8 -*-
from .method.descriptor import Method as MethodObserver
from .attribute.descriptor import Attribute as AttributeObserver
from .events.subject import Subject
from types import BuiltinFunctionType, BuiltinMethodType, FunctionType, LambdaType, MethodType

__all__ = ['Observable', 'MethodObserver', 'AttributeObserver', 'Observer', 'Subject']


def Observable(cls):
    fields = filter(lambda attr: not attr[0].startswith('_'), cls.__dict__.items())
    for attr, value in fields:
        setattr(cls, attr, Observer(value))
    return Subject(cls)

def Observer(value):
    if is_a_method(value):
        return MethodObserver(value)
    return AttributeObserver(value)


def is_a_method(method):
    return isinstance(
        method,
        (BuiltinFunctionType, BuiltinMethodType, FunctionType, LambdaType, MethodType)
    )

