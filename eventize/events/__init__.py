# -*- coding: utf8 -*-
from .handler import Handler
from .event import Event
from .subject import Subject

__all__ = ['Handler', 'Event', 'Subject']


def listen(observer, event_type, handler=None):
    channel = event_type.__name__
    if handler is None:
        handler = getattr(observer, channel, Handler())
    elif hasattr(observer, channel):
        handler.extend(getattr(observer, channel))
    setattr(handler, 'event_type', event_type)
    setattr(observer, channel, handler)
    return handler


def notify(observer, event):
    channel = type(event).__name__
    if hasattr(observer, channel):
        return getattr(observer, channel).propagate(event)
    return event

