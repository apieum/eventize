# -*- coding: utf8 -*-

class StopPropagation(UserWarning):
    pass

class Slot(list):
    def __init__(self, *func_list):
        self._assert_list_valid(func_list)
        self.events = []
        list.__init__(self, func_list)

    def __call__(self, event):
        self.events.append(event)
        try:
            self.propagate(event)
        except StopPropagation:
            pass
        return event.result


    def propagate(self, event):
        for func in self:
            func(event)
        return event

    def when(self, condition):
        from conditional import Conditional
        cond = Conditional(condition=condition)
        self.append(cond)
        return cond

    def called_with(self, *expected_args, **expected_kwargs):
        def condition(event):
            for arg in expected_args:
                if not event.has_arg(arg):
                    return False
            for key, item in list(expected_kwargs.items()):
                if not event.has_kwarg(key, item):
                    return False
            return True
        return self.when(condition)

    def __iadd__(self, func):
        self.append(func)
        return self

    def __isub__(self, func):
        while func in self:
            self.remove(func)
        return self

    def __repr__(self):
        return type(self)

    def __setitem__(self, key, func):
        self._assert_valid(func)
        return list.__setitem__(self, key, func)

    def append(self, func):
        self._assert_valid(func)
        list.append(self, func)
        return self

    do = append

    def insert(self, key, func):
        self._assert_valid(func)
        return list.insert(self, key, func)

    def extend(self, func_list):
        self._assert_list_valid(func_list)
        return list.extend(self, func_list)

    def _assert_list_valid(self, enumerable):
        for value in enumerable:
            self._assert_valid(value)

    def _assert_valid(self, func):
        if not callable(func):
            raise TypeError('"%s": is not calable' % func)

