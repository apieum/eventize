# -*- coding: utf8 -*-
from .exceptions import StopPropagation
from .event import Event, AttributeEvent, MethodEvent
from ..namedDescriptor import NamedDescriptor


class Handler(list):
    event_class = Event
    def __init__(self, *callback_list, **options):
        self.extend(list(callback_list))
        self.events = []
        condition = options.get('condition', lambda event: True)
        self._assert_valid(condition)
        self.condition = condition

    def call(self, subject, *args, **kwargs):
        event = self.make_event(subject, *args, **kwargs)
        self.__call__(event)
        return event

    def __call__(self, event):
        self.events.append(event)
        try:
            self.propagate(event)
        except StopPropagation:
            pass
        return event.returns()

    def make_event(self, subject, *args, **kwargs):
        return self.event_class(subject, *args, **kwargs)

    def propagate(self, event):
        self._assert_condition(event)
        self.before_propagation(event)
        for callback in self:
            event.trigger(callback)
        self.after_propagation(event)
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
    handler_class = Handler
    def get(self, instance, alias):
        if not self.is_set(instance, alias):
            instance.__dict__[alias] = self.make_handler(instance, alias)
        return instance.__dict__[alias]

    def set(self, instance, alias, value):
        instance.__dict__[alias] = value

    def delete(self, instance, alias):
        del instance.__dict__[alias]

    def make_handler(self, instance, alias):
        handler = self.handler_class(condition=self.condition)
        handler.__alias__ = alias
        handler.parent = self
        return handler

    def __hash__(self):
        return id(self)

class InstanceHandler(Handler):
    event_class = MethodEvent
    def before_propagation(self, event):
        if hasattr(self, 'parent'):
            self.parent(event)
        if hasattr(self, 'parentInstance'):
            self.parentInstance(event)

class AttributeHandler(DescriptorHandler):
    event_class = AttributeEvent
    class handler_class(Handler):
        event_class = AttributeEvent
        def before_propagation(self, event):
            if hasattr(self, 'parent'):
                self.parent(event)

        def after_propagation(self, event):
            alias = getattr(self, '__alias__', '')
            handler = getattr(event.value, alias, lambda event: event)
            handler(event)

class MethodHandler(DescriptorHandler):
    event_class = MethodEvent
