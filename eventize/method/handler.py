# -*- coding: utf8 -*-
from .. import events, descriptors
from .event import BeforeEvent, AfterEvent

class Before(events.Handler):
    event_type = BeforeEvent

class After(events.Handler):
    event_type = AfterEvent


class BeforeHandler(descriptors.Handler):
    default = Before

class AfterHandler(descriptors.Handler):
    default = After

Subject = events.Subject(BeforeHandler, AfterHandler)
