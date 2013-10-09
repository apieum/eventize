# -*- coding: utf8 -*-
from . import EventSlot, Event

class Listener(object):
    __events__ = []

    _null_trigger = lambda self, event: None
    trigger = lambda self, this, event_name, event: getattr(this, event_name, self._null_trigger)(event)


    def _make_event(self, instance, *args, **kwargs):
        return Event(instance, *args, **kwargs)

    def _create_events(self, instance, copy_from=None):
        events = {}
        for event_name in self.__events__:
            events[event_name] = getattr(copy_from, event_name, EventSlot())
        return events

    def _attach_events(self, instance, events):
        for event_name, event in events.items():
            setattr(instance, event_name, event)

    def _set_events(self, instance, copy_from=None):
        events = self._create_events(instance, copy_from)

        try:
            self._attach_events(instance, events)
        except AttributeError:
            instance = self._subtype_instance(instance, events)
        return instance

    def _subtype_instance(self, instance, events):
        instance_type = type(instance)
        bases = (instance_type, ) + instance_type.__bases__
        attrs = dict(instance_type.__dict__)
        attrs.update(events)
        try:
            return type(instance_type.__name__, bases, attrs)(instance)
        except TypeError:
            return instance

    def clear(self):
        for event_name in self.__events__:
            getattr(self, event_name).remove_all()
