# -*- coding: utf8 -*-
from .. import events, descriptors
from .event import BeforeEvent, AfterEvent

class Handler(descriptors.Handler):
    pass

class Before(events.Handler):
    event_type = BeforeEvent

class After(events.Handler):
    event_type = AfterEvent

Subject = events.Subject(Handler)
