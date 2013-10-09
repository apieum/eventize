# -*- coding: utf8 -*-
from . import EventSlot, Event

class Listener(object):
    __events__ = []

    trigger = lambda self, event_name, event: getattr(self, event_name, self._null_trigger)(event)

    _null_trigger = lambda self, event:None

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

    def _attach_trigger(self, instance, copy_from=None):
        if hasattr(copy_from, 'trigger'):
            trigger = getattr(copy_from, 'trigger')
        else:
            trigger = lambda event_name, event: getattr(instance, event_name, self._null_trigger)(event)
        setattr(instance, 'trigger', trigger)

    def _set_events(self, instance, copy_from=None):
        events = self._create_events(instance, copy_from)

        try:
            self._attach_events(instance, events)
            self._attach_trigger(instance, copy_from)
        except AttributeError:
            try:
                instance = self._subtype_instance(instance, events)
                self._attach_trigger(instance, copy_from)
            except TypeError:
                pass
        return instance

    def _subtype_instance(self, instance, events):
            instance_type = type(instance)
            bases = (instance_type, ) + instance_type.__bases__
            attrs = dict(instance_type.__dict__)
            attrs.update(events)
            return type(instance_type.__name__, bases, attrs)(instance)

    def clear(self):
        for event_name in self.__events__:
            getattr(self, event_name).remove_all()
