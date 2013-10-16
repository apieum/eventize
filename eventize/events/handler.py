# -*- coding: utf8 -*-
from .event import Event
from ..namedDescriptor import NamedDescriptor


class StopPropagation(UserWarning):
    pass

class Handler(list):
    def __init__(self, *callback_list, **options):
        self._assert_list_valid(callback_list)
        self.events = []
        condition = options.get('condition', lambda event: True)
        self._assert_valid(condition)
        self.condition = condition
        list.__init__(self, callback_list)

    def trigger(self, event):
        self.events.append(event)
        try:
            self.propagate(event)
        except StopPropagation:
            pass
        return event.result


    def __call__(self, subject, *args, **kwargs):
        if isinstance(subject, Event):
            event = subject
        else:
            event = self.make_event(subject, *args, **kwargs)
        self.trigger(event)
        return event

    def make_event(self, subject, *args, **kwargs):
        return Event(subject, *args, **kwargs)

    def propagate(self, event):
        if not self.condition(event):
            msg = "Condition '%s' for event '%s' return False" % (id(self.condition), event.__type__)
            event.stop_propagation(msg)
        for callback in self:
            event.trigger(callback)
        return event

    def when(self, condition):
        cond = type(self)(condition=condition)
        self.append(cond)
        return cond

    def append(self, callback):
        self._assert_valid(callback)
        list.append(self, callback)
        return self

    do = append
    then = append

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



class DescriptorHandler(Handler, NamedDescriptor):
    def get(self, instance, name):
        if not self.is_set(instance, name):
            instance.__dict__[name] = type(self)()
        return instance.__dict__[name]

    def set(self, instance, name, value):
        instance.__dict__[name] = value

    def delete(self, instance, name):
        del instance.__dict__[name]

    def __call__(self, subject, *args, **kwargs):
        if isinstance(subject, Event):
            event = subject
        else:
            event = self.make_event(subject, *args, **kwargs)

        # self.triggerClass(event)
        self.trigger(event)
        self.triggerValue(event)
        return event

    def triggerClass(self, event):
        attribute = getattr(type(event.subject), event.name)
        name = self.get_name(self)
        if name is not None:
            handler = attribute.__dict__.get(name)
            handler.trigger(event)

    def triggerValue(self, event):
        name = self.get_name(self)
        if name is not None and hasattr(event.value, '__dict__'):
            handler = event.value.__dict__.get(name)
            if hasattr(handler, 'trigger'):
                handler.trigger(event)


    def __hash__(self):
        return id(self)

class OnGetHandler(DescriptorHandler):
    __name__= 'on_get'
    def make_event(self, subject, name):
        return Event(subject, name=name, value=subject.__dict__[name], __type__=self.__name__)

class OnSetHandler(DescriptorHandler):
    __name__ = 'on_set'
    def make_event(self, subject, name, value):
        old_value = subject.__dict__.get(name, None)
        value = self.set_events(value, old_value)
        return Event(subject, name=name, value=value, __type__=self.__name__)

    def set_events(self, subject, copy_from=None):
        on_get = getattr(copy_from, 'on_get', OnGetHandler())
        on_set = getattr(copy_from, 'on_set', OnSetHandler())
        on_del = getattr(copy_from, 'on_del', OnDelHandler())
        try:
            setattr(subject, 'on_get', on_get)
            setattr(subject, 'on_set', on_set)
            setattr(subject, 'on_del', on_del)
        except AttributeError:
            subject = self.subtype_subject(subject, on_get=on_get, on_set=on_set, on_del=on_del)
        return subject

    def subtype_subject(self, subject, **handlers):
        subject_type = type(subject)
        bases = (subject_type, ) + subject_type.__bases__
        attrs = dict(subject_type.__dict__)
        attrs['on_get'] = OnGetHandler()
        attrs['on_set'] = OnSetHandler()
        attrs['on_del'] = OnDelHandler()
        try:
            result = type(subject_type.__name__, bases, attrs)(subject)
            for handler_name, handler in handlers.items():
                result.__dict__[handler_name] = handler
            return result
        except TypeError:
            return subject


class OnDelHandler(DescriptorHandler):
    __name__= 'on_del'
    def make_event(self, subject, name):
        return Event(subject, name=name, value=subject.__dict__[name], __type__=self.__name__)


class BeforeHandler(DescriptorHandler):
    __name__='before'
    def make_event(self, subject, *args, **kwargs):
        event = Event(subject, *args, **kwargs)
        event.__type__ = self.__name__
        return event

    def triggerValue(self, event):
        pass


class AfterHandler(DescriptorHandler):
    __name__='after'
    def make_event(self, subject, *args, **kwargs):
        event = Event(subject, *args, **kwargs)
        event.__type__ = self.__name__
        return event

    def triggerValue(self, event):
        pass
