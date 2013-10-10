# -*- coding: utf8 -*-

class StopPropagation(UserWarning):
    pass

class Handler(list):
    def __init__(self, *callback_list):
        self._assert_list_valid(callback_list)
        self.events = []
        list.__init__(self, callback_list)

    def __call__(self, event):
        self.events.append(event)
        try:
            self.propagate(event)
        except StopPropagation:
            pass
        return event.result


    def propagate(self, event):
        for callback in self:
            event.trigger(callback)
        return event

    def when(self, condition):
        from .conditional import Conditional
        cond = Conditional(condition=condition)
        self.append(cond)
        return cond

    def called_with(self, *expected_args, **expected_kwargs):
        def condition(event):
            for arg in expected_args:
                if not event.arg_equal(arg):
                    return False
            for key, item in list(expected_kwargs.items()):
                if not event.kwarg_equal(key, item):
                    return False
            return True
        return self.when(condition)

    def called_with_instance_of(self, **expected_kwargs_types):
        def condition(event):
            for key, expected_type in list(expected_kwargs_types.items()):
                if not event.is_kwarg_instance_of(key, expected_type):
                    return False
            return True
        return self.when(condition)

    def called_with_type(self, **expected_kwargs_types):
        def condition(event):
            for key, expected_type in list(expected_kwargs_types.items()):
                if not event.is_kwarg_type_equal(key, expected_type):
                    return False
            return True
        return self.when(condition)

    def append(self, callback):
        self._assert_valid(callback)
        list.append(self, callback)
        return self

    do = append

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
        return type(self)

    def __setitem__(self, key, callback):
        self._assert_valid(callback)
        return list.__setitem__(self, key, callback)

