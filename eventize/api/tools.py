# -*- coding: utf8 -*-
from types import BuiltinFunctionType, BuiltinMethodType, FunctionType, LambdaType, MethodType
from . import Method

methods = (Method, BuiltinFunctionType, BuiltinMethodType, FunctionType, LambdaType, MethodType)
is_a_method = lambda method: isinstance(method, methods)
