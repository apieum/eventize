# -*- coding: utf8 -*-
from .. import descriptors, events
from .event import OnGetEvent, OnSetEvent, OnDelEvent, OnChangeEvent

class OnGet(events.Handler):
    event_type = OnGetEvent

class OnSet(events.Handler):
    event_type = OnSetEvent

class OnDel(events.Handler):
    event_type = OnDelEvent

class OnChange(events.Handler):
    event_type = OnChangeEvent

class OnGetDescriptor(descriptors.Handler):
    default = OnGet

class OnSetDescriptor(descriptors.Handler):
    default = OnSet

class OnDelDescriptor(descriptors.Handler):
    default = OnDel

class OnChangeDescriptor(descriptors.Handler):
    default = OnChange


Subject = events.Subject(OnGetDescriptor, OnSetDescriptor, OnDelDescriptor, OnChangeDescriptor)
