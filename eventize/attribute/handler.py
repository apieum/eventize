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

class OnGetHandler(descriptors.Handler):
    __alias__ = 'on_get'
    default = OnGet

class OnSetHandler(descriptors.Handler):
    __alias__ = 'on_set'
    default = OnSet

class OnDelHandler(descriptors.Handler):
    __alias__ = 'on_del'
    default = OnDel

class OnChangeHandler(descriptors.Handler):
    __alias__ = 'on_change'
    default = OnChange


Subject = events.Subject(OnGetHandler, OnSetHandler, OnDelHandler, OnChangeHandler)
