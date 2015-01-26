# -*- coding: utf8 -*-
from .handler import Handler
from .event import Event
from .subject import Subject

__all__ = ['Handler', 'Event', 'Subject', 'notify', 'listen', 'stop_listen','on_notify_error']

on_notify_error = Handler()

def listen(observer, channel, handler=None):
    listen = dict(getattr(observer, '__listen__', {}))
    if handler is None:
        if channel in listen: return listen.get(channel)
        handler = Handler()
    handler.extend(listen.get(channel, []))
    listen[channel] = handler
    setattr(observer, '__listen__', listen)
    return handler

def notify(observer, event):
    channel = event.__channel__
    listen = getattr(observer, '__listen__', {channel: on_notify_error})
    return listen.get(channel).propagate(event)

def stop_listen(observer, channel):
    listen = getattr(observer, '__listen__', {})
    return listen.pop(channel, [])

