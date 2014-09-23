# -*- coding: utf8 -*-
from ..typing import MethodDescriptor
from .. import descriptors
from .handler import BeforeHandler, AfterHandler
from .value import Value

class Descriptor(MethodDescriptor, descriptors.Named):
    ValueType = Value
    before = BeforeHandler()
    after = AfterHandler()

