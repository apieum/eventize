# -*- coding: utf8 -*-
from .abstract import abstract, abstractmethod

@abstract
class Visitor(object):
    """Visitor for handlers or descriptors"""
    @abstractmethod
    def visit(self, visited):
        """do something on visited"""

@abstract
class Modifier(Visitor):
    """Visitor with rollback"""
    @abstractmethod
    def restore(self, visited):
        """restore visited state"""


@abstract
class Visitable(object):
    """Visitable"""
    visitors = tuple()

    def is_visitor(self, visitor):
        return isinstance(visitor, Visitor)

    def accept_all(self, *visitors):
        return tuple(map(self.accept, visitors))

    def accept(self, visitor):
        """apply visitor"""
        self.visitors+= (visitor, )
        return visitor.visit(self) if self.is_visitor(visitor) else self.reject(visitor)

    @abstractmethod
    def reject(self, visitor):
        """What to do if visitor is not a Visitor"""


@abstract
class Modifiable(Visitable):
    """Visitable with deny (rollback)"""

    def is_modifier(self, visitor):
        return isinstance(visitor, Modifier)

    def deny_all(self):
        if len(self.visitors) > 0:
            return self.deny(self.visitors[0])

    def deny(self, visitor):
        """deny visitor"""
        visitors = self.rollback(visitor)
        visitors.pop()
        self.accept_all(*visitors)

    def rollback(self, visitor):
        if visitor not in self.visitors: return
        index = self.visitors.index(visitor)
        visitors = list(self.visitors[index:])
        visitors.reverse()
        tuple(map(self.expunge, visitors))
        return visitors

    def expunge(self, visitor):
        self.remove_visitor(visitor)
        return visitor.restore(self) if self.is_modifier(visitor) else self.defer(visitor)

    def remove_visitor(self, visitor):
        if visitor in self.visitors:
            visitors = list(self.visitors)
            visitors.remove(visitor)
            self.visitors = tuple(visitors)

    @abstractmethod
    def defer(self, visitor):
        """What to do if visitor is not a Modifier"""
