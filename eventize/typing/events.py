# -*- coding: utf8 -*-

class AbstractEvent(object):
    messages = []
    results = []
    def trigger(self, callback):
        """call callback with self and append result to self.results"""
        raise NotImplementedError("AbstractEvent.trigger must be overriden")

    def stop_propagation(self, msg=None):
        """Append msg to self.messages and raise StopPropagation user warning"""
        raise NotImplementedError("AbstractEvent.stop_propagation must be overriden")

    def returns(self):
        """Result of successive calls of event (by default self)"""
        raise NotImplementedError("AbstractEvent.returns must be overriden")

class AbstractHandler(list):
    """list which contains callbacks"""
    event_type = AbstractEvent

    def condition(self):
        """Function to test if can propagate by default always True"""
        raise NotImplementedError("AbstractHandler.condition must be overriden")

    def clear_events(self):
        """remove all passed events (self.events)"""
        raise NotImplementedError("AbstractHandler.clear_events must be overriden")

    def empty(self):
        """remove all callbacks"""
        raise NotImplementedError("AbstractHandler.empty must be overriden")

    def clear(self):
        """empty list and clear events"""
        raise NotImplementedError("AbstractHandler.clear must be overriden")

    def when(self, condition):
        """return conditionnal observer, create it before of not exists"""
        raise NotImplementedError("AbstractHandler.when must be overriden")

    def do(self, callback):
        """append callback to self if callable"""
        raise NotImplementedError("AbstractHandler.do must be overriden")

    def then(self, callback):
        """alias of do"""
        raise NotImplementedError("AbstractHandler.then must be overriden")

    def notify(self, *args, **kwargs):
        """Create and return an event after its propagation"""
        raise NotImplementedError("AbstractHandler.notify must be overriden")

    def make_event(self, *args, **kwargs):
        """make an event of self.event_type"""
        raise NotImplementedError("AbstractHandler.make_event must be overriden")

    def __call__(self, event):
        """Propagate event then return event.result"""
        raise NotImplementedError("AbstractHandler.__call__ must be overriden")

    def propagate(self, event):
        """call event.trigger for each callbacks of self and return event"""
        raise NotImplementedError("AbstractHandler.propagate must be overriden")
