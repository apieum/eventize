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
    default = OnGet

class OnSetHandler(descriptors.Handler):
    default = OnSet

class OnDelHandler(descriptors.Handler):
    default = OnDel

class OnChangeHandler(descriptors.Handler):
    default = OnChange


Subject = events.Subject(OnGetHandler, OnSetHandler, OnDelHandler, OnChangeHandler)
