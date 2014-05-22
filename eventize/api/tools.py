# -*- coding: utf8 -*-
from types import BuiltinFunctionType, BuiltinMethodType, FunctionType, LambdaType, MethodType
from ..method import Method
from ..attribute import Attribute

__all__ = ['Attribute', 'Method', 'is_a_method']

methods = (Method, BuiltinFunctionType, BuiltinMethodType, FunctionType, LambdaType, MethodType)
is_a_method = lambda method: isinstance(method, methods)
