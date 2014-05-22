# -*- coding: utf8 -*-
from .. import events, descriptors
from .event import BeforeEvent, AfterEvent

class Before(events.Handler):
    event_type = BeforeEvent

class After(events.Handler):
    event_type = AfterEvent


class BeforeDescriptor(descriptors.Handler):
    default = Before

class AfterDescriptor(descriptors.Handler):
    default = After

Subject = events.Subject(Before, After)
