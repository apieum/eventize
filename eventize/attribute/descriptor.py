# -*- coding: utf8 -*-
from .. import descriptors
from .handler import OnGetHandler, OnSetHandler, OnDelHandler, OnChangeHandler
from .value import Value

class Descriptor(descriptors.Named):
    ValueType = Value
    on_get = OnGetHandler()
    on_set = OnSetHandler()
    on_del = OnDelHandler()
    on_change = OnChangeHandler()
