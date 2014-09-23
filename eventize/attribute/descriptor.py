# -*- coding: utf8 -*-
from ..typing import AttributeDescriptor
from .. import descriptors
from .handler import OnGetHandler, OnSetHandler, OnDelHandler, OnChangeHandler
from .value import Value

class Descriptor(AttributeDescriptor, descriptors.Named):
    ValueType = Value
    on_get = OnGetHandler()
    on_set = OnSetHandler()
    on_del = OnDelHandler()
    on_change = OnChangeHandler()
