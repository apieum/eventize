# -*- coding: utf8 -*-
from .exceptions import StopPropagation
from .event import Event


class EventType(object):
    def __init__(self, event_type):
        self.event_type = event_type
    def visit(self, handler):
        handler.event_type = self.event_type


class Handler(list):
    event_type = Event
    def __init__(self, *callbacks, **options):
        self.events = []
        condition = options.get('condition', lambda event: True)
        self._assert_valid(condition)
        self.condition = condition
        list(map(self.visit, callbacks))

    def visit(self, callback):
        visit = getattr(callback, 'visit', lambda *a: self.append(callback))
        return visit(self)

    def notify(self, *args, **kwargs):
        event = self.make_event(*args, **kwargs)
        return self.propagate(event)

    def make_event(self, *args, **kwargs):
        return self.event_type(*args, **kwargs)

    def __call__(self, event):
        return self.propagate(event).returns()

    def propagate(self, event):
        self.events.append(event)
        try:
            self._assert_condition(event)
            self.before_propagation(event)
            list(map(event.trigger, self))
            self.after_propagation(event)
        except StopPropagation:
            pass
        return event

    def before_propagation(self, event):
        pass
    def after_propagation(self, event):
        pass

    def _assert_condition(self, event):
        if not self.condition(event):
            msg = "Condition '%s' for event '%s' return False" % (id(self.condition), type(event).__name__)
            event.stop_propagation(msg)

    def when(self, condition):
        cond = type(self)(condition=condition)
        self.append(cond)
        return cond

    def append(self, callback):
        self._assert_valid(callback)
        list.append(self, callback)
        return self

    def prepend(self, callbacks_list):
        currents = list(self)
        self.empty()
        self.extend(callbacks_list)
        list.extend(self, currents)
        return self

    def insert(self, key, callback):
        self._assert_valid(callback)
        return list.insert(self, key, callback)

    def extend(self, callback_list):
        self._assert_list_valid(callback_list)
        return list.extend(self, callback_list)

    def clear_events(self):
        self.events=[]

    def empty(self):
        del self[0:]

    def clear(self):
        self.clear_events()
        self.empty()

    def _assert_list_valid(self, enumerable):
        list(map(self._assert_valid, enumerable))

    def _assert_valid(self, func):
        if not callable(func):
            raise TypeError('"%s": is not callable' % func)

    def __iadd__(self, callback):
        self.append(callback)
        return self

    def __isub__(self, callback):
        while callback in self:
            self.remove(callback)
        return self

    def __repr__(self):
        return "%s: %s" % (type(self).__name__, list(self).__repr__())

    def __setitem__(self, key, callback):
        self._assert_valid(callback)
        return list.__setitem__(self, key, callback)

    do = then = append

