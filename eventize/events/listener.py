# -*- coding: utf8 -*-
from .handler import Handler
from .event import Event

class Listener(object):
    __events__ = []
    __listen__ = {}

    _null_trigger = lambda self, event: None
    trigger = lambda self, this, event_name, event: getattr(this, event_name, self._null_trigger)(event)


    def _make_event(self, subject, *args, **kwargs):
        return Event(subject, *args, **kwargs)

    def _create_events(self, subject, copy_from=None):
        events = {}
        listen = getattr(subject, '__listen__', {})
        for event_name in self.__events__:
            events[event_name] = getattr(copy_from, event_name, Handler(*listen.get(event_name, tuple())))
        return events

    def _attach_events(self, subject, events):
        for event_name, event in events.items():
            setattr(subject, event_name, event)

    def _set_events(self, subject, copy_from=None):
        events = self._create_events(subject, copy_from)

        try:
            self._attach_events(subject, events)
        except AttributeError:
            subject = self._subtype_subject(subject, events)
        return subject

    def _subtype_subject(self, subject, events):
        subject_type = type(subject)
        bases = (subject_type, ) + subject_type.__bases__
        attrs = dict(subject_type.__dict__)
        attrs.update(events)
        try:
            return type(subject_type.__name__, bases, attrs)(subject)
        except TypeError:
            return subject

    def clear(self):
        for event_name in self.__events__:
            getattr(self, event_name).remove_all()
