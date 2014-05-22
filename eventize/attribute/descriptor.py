# -*- coding: utf8 -*-
from .. import descriptors
from .handler import OnGetDescriptor, OnSetDescriptor, OnDelDescriptor, OnChangeDescriptor
from .value import Value

class Descriptor(descriptors.Named):
    ValueType = Value
    on_get = OnGetDescriptor()
    on_set = OnSetDescriptor()
    on_del = OnDelDescriptor()
    on_change = OnChangeDescriptor()
