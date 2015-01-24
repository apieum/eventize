# -*- coding: utf8 -*-

from collections import deque


class Checked(object):
    def __init__(self, items=[], check=None, fallback=None):
        self._items = deque()
        if callable(check):
            self.check = check
        if callable(fallback):
            self.fallback = fallback
        self.push_all(items)

    def push(self, item):
        if not self.check(item):
            item = self.fallback(item)
        self._items.appendleft(item)
        return item

    def push_all(self, items):
        return tuple(map(self.push, items))

    def pop(self):
        return self._items.popleft()

    def __getitem__(self, index):
        if isinstance(index, slice):
            return deque(list(self._items)[index])
        return self._items[index]

    def __contains__(self, item):
        return item in self._items

    def __len__(self):
        return len(self._items)

    def index(self, item):
        return tuple(self._items).index(item)

    def remove(self, item):
        if item not in self:
            raise ValueError("remove(item): %s not in %s" %(item, self))
        self._items.remove(item)

    def check(self, item):
        raise NotImplementedError("stack.Checked.check must be overriden")

    def fallback(self, item):
        raise NotImplementedError("stack.Checked.fallback must be overriden")
