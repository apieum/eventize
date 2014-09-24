# -*- coding: utf8 -*-
from .abstract import abstract, abstractmethod, abstractproperty

@abstract
class AbstractEvent(object):
    messages = []
    results = []
    @abstractmethod
    def trigger(self, callback):
        """call callback with self and append result to self.results"""

    @abstractmethod
    def stop_propagation(self, msg=None):
        """Append msg to self.messages and raise StopPropagation user warning"""

    @abstractmethod
    def returns(self):
        """Result of successive calls of event (by default self)"""

@abstract
class AbstractHandler(list):
    """list which contains callbacks"""
    event_type = AbstractEvent

    @abstractproperty
    def condition(self):
        """Function to test if can propagate by default always True"""

    @abstractmethod
    def clear_events(self):
        """remove all passed events (self.events)"""

    @abstractmethod
    def empty(self):
        """remove all callbacks"""

    @abstractmethod
    def clear(self):
        """empty list and clear events"""

    @abstractmethod
    def do(self, callback):
        """append callback if callable to self"""

    @abstractmethod
    def then(self, callback):
        """alias of do"""

    @abstractmethod
    def notify(self, *args, **kwargs):
        """Create and return an event after its propagation"""

    @abstractmethod
    def make_event(self, *args, **kwargs):
        """make an event of self.event_type"""

    @abstractmethod
    def __call__(self, event):
        """Propagate event then return event.result"""

    @abstractmethod
    def propagate(self, event):
        """call event.trigger for each callbacks of self and return event"""
