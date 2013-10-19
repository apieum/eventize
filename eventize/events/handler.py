# -*- coding: utf8 -*-
from .exceptions import StopPropagation
from .event import Event, AttributeEvent, MethodEvent
from ..namedDescriptor import NamedDescriptor


class Handler(list):
    def __init__(self, *callback_list, **options):
        self._assert_list_valid(callback_list)
        self.events = []
        condition = options.get('condition', lambda event: True)
        self._assert_valid(condition)
        self.condition = condition
        list.__init__(self, callback_list)

    def call(self, subject, *args, **kwargs):
        event = self.make_event(subject, *args, **kwargs)
        self.__call__(event)
        return event

    def __call__(self, event):
        self.events.append(event)
        try:
            event = self.propagate(event)
        except StopPropagation:
            pass
        return event.returns()

    def make_event(self, subject, *args, **kwargs):
        return Event(subject, *args, **kwargs)

    def propagate(self, event):
        self._assert_condition(event)
        return self.trigger_all(self, event)

    def trigger_all(self, handler, event):
        for callback in handler:
            event.trigger(callback)
        return event

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

    def insert(self, key, callback):
        self._assert_valid(callback)
        return list.insert(self, key, callback)

    def extend(self, callback_list):
        self._assert_list_valid(callback_list)
        return list.extend(self, callback_list)

    def remove_events(self):
        self.events=[]

    def remove_observers(self):
        del self[0:]

    def remove_all(self):
        self.remove_events()
        self.remove_observers()

    def _assert_list_valid(self, enumerable):
        for value in enumerable:
            self._assert_valid(value)

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



class DescriptorHandler(Handler, NamedDescriptor):
    def get(self, instance, alias):
        if not self.is_set(instance, alias):
            instance.__dict__[alias] = type(self)()
            instance.__dict__[alias].__alias__ = alias
        return instance.__dict__[alias]

    def set(self, instance, alias, value):
        instance.__dict__[alias] = value

    def delete(self, instance, alias):
        del instance.__dict__[alias]

    def __hash__(self):
        return id(self)


class AttributeHandler(DescriptorHandler):
    def propagate(self, event):
        event = super(AttributeHandler, self).propagate(event)
        return self.trigger_value(event)

    def trigger_value(self, event):
        handler = self.value_handler(event)
        if handler is not self and isinstance(handler, Handler):
            handler(event)
        return event

    def value_handler(self, event):
        alias = self.__alias__
        if self._contains_handler(alias, event.value):
            return event.value.__dict__[alias]

    def _contains_handler(self, alias, value):
        return hasattr(value, '__dict__') and alias in value.__dict__


    def make_event(self, subject, *args, **kwargs):
        return AttributeEvent(subject, *args, **kwargs)

class MethodHandler(DescriptorHandler):
    def make_event(self, subject, *args, **kwargs):
        return MethodEvent(subject, *args, **kwargs)
