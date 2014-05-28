# -*- coding: utf8 -*-
from .exceptions import StopPropagation
from .event import Event


class EventType(object):
    def __init__(self, event_type):
        self.event_type = event_type
    def visit(self, handler):
        handler.event_type = self.event_type

def always_true(event):
    return True

class Handler(list):
    event_type = Event
    def __init__(self, *callbacks, **options):
        self.events = tuple()
        for item, value in tuple(options.items()):
            setattr(self, item, value)

        if not hasattr(self, 'condition'):
            self.condition = always_true

        self._assert_valid(self.condition)
        self.visitors = tuple(map(self.apply, callbacks))

    def apply(self, callback):
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
        self.events = self.events + (event, )
        try:
            getattr(self, 'before_propagation', always_true)(event)
            self._assert_condition(event)
            tuple(map(event.trigger, self))
            getattr(self, 'after_propagation', always_true)
        except StopPropagation:
            pass
        return event

    def _assert_condition(self, event):
        if not self.condition(event):
            msg = "Condition '%s' for event '%s' return False" % (id(self.condition), type(event).__name__)
            event.stop_propagation(msg)

    def when(self, condition):
        cond = type(self)(condition=condition)
        try:
            index = self.index(cond)
        except ValueError:
            index = len(self)
            self.append(cond)
        return self[index]

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
        self.events = tuple()

    def empty(self):
        del self[0:]

    def clear(self):
        self.clear_events()
        self.empty()

    def _assert_list_valid(self, enumerable):
        tuple(map(self._assert_valid, enumerable))

    def _assert_valid(self, func):
        if not callable(func):
            raise TypeError('"%s": is not callable' % func)

    def __setitem__(self, key, callback):
        self._assert_valid(callback)
        super(Handler, self).__setitem__(key, callback)

    def __iadd__(self, callback):
        self.append(callback)
        return self

    def __isub__(self, callback):
        while callback in self:
            self.remove(callback)
        return self

    def __repr__(self):
        return "%s: %s" % (type(self).__name__, list(self).__repr__())

    def __eq__(self, other):
        cond1 = getattr(self, 'condition', None)
        cond2 = getattr(other, 'condition', None)
        return cond1 == cond2

    def __setitem__(self, key, callback):
        self._assert_valid(callback)
        return list.__setitem__(self, key, callback)

    do = then = append

