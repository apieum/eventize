# -*- coding: utf8 -*-
from .. import descriptors, events
from .event import OnGetEvent, OnSetEvent, OnDelEvent, OnChangeEvent

class Handler(descriptors.Handler):
    pass

class OnGet(events.Handler):
    event_type = OnGetEvent

class OnSet(events.Handler):
    event_type = OnSetEvent

class OnDel(events.Handler):
    event_type = OnDelEvent

class OnChange(events.Handler):
    event_type = OnChangeEvent



Subject = events.Subject(Handler)
