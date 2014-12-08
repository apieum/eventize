# -*- coding: utf8 -*-

from collections import deque

class Visitor(object):
    """Visitor for handlers or descriptors"""
    def visit(self, visited):
        """do something on visited"""
        raise NotImplemented()

class Modifier(Visitor):
    """Visitor with rollback"""
    def restore(self, visited):
        """restore visited state"""
        raise NotImplemented()


class Visitable(object):
    """Visitable"""
    def __init__(self):
        self.visitors = deque()

    def is_visitor(self, visitor):
        return isinstance(visitor, Visitor)

    def accept_all(self, *visitors):
        return tuple(map(self.accept, visitors))

    def accept(self, visitor):
        """apply visitor"""
        if self.is_visitor(visitor):
            visitor.visit(self)
            self.visitors.appendleft(visitor)
        else:
            self.reject(visitor)
        return visitor

    def reject(self, visitor):
        """What to do if visitor is not a Visitor"""
        raise NotImplemented()


class Modifiable(Visitable):
    """Visitable with deny (rollback)"""

    def is_modifier(self, visitor):
        return isinstance(visitor, Modifier)

    def deny_all(self):
        if len(self.visitors) > 0:
            return self.rollback_to(len(self.visitors))

    def deny(self, visitor):
        """deny visitor"""
        visitors = self.rollback(visitor)
        visitors.pop()
        self.accept_all(*reversed(visitors))

    def rollback(self, visitor):
        if visitor not in self.visitors: return deque()
        index = tuple(self.visitors).index(visitor)
        return self.rollback_to(index)

    def rollback_to(self, index):
        return deque(map(self.expunge, tuple(self.visitors)[:index+1]))

    def expunge(self, visitor):
        if self.is_modifier(visitor):
            visitor.restore(self)
            self.remove_visitor(visitor)
        else:
            self.defer(visitor)
        return visitor

    def remove_visitor(self, visitor):
        if visitor in self.visitors:
            self.visitors.remove(visitor)

    def defer(self, visitor):
        """What to do if visitor is not a Modifier"""
        raise NotImplemented()
