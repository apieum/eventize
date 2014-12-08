# -*- coding: utf8 -*-

class AbstractEvent(object):
    messages = []
    results = []
    def trigger(self, callback):
        """call callback with self and append result to self.results"""
        raise NotImplemented()

    def stop_propagation(self, msg=None):
        """Append msg to self.messages and raise StopPropagation user warning"""
        raise NotImplemented()

    def returns(self):
        """Result of successive calls of event (by default self)"""
        raise NotImplemented()

class AbstractHandler(list):
    """list which contains callbacks"""
    event_type = AbstractEvent

    def condition(self):
        """Function to test if can propagate by default always True"""
        raise NotImplemented()

    def clear_events(self):
        """remove all passed events (self.events)"""
        raise NotImplemented()

    def empty(self):
        """remove all callbacks"""
        raise NotImplemented()

    def clear(self):
        """empty list and clear events"""
        raise NotImplemented()

    def when(self, condition):
        """return conditionnal observer, create it before of not exists"""
        raise NotImplemented()

    def do(self, callback):
        """append callback to self if callable"""
        raise NotImplemented()

    def then(self, callback):
        """alias of do"""
        raise NotImplemented()

    def notify(self, *args, **kwargs):
        """Create and return an event after its propagation"""
        raise NotImplemented()

    def make_event(self, *args, **kwargs):
        """make an event of self.event_type"""
        raise NotImplemented()

    def __call__(self, event):
        """Propagate event then return event.result"""
        raise NotImplemented()

    def propagate(self, event):
        """call event.trigger for each callbacks of self and return event"""
        raise NotImplemented()
