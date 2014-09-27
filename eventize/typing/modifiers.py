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
        if self.is_visitor(visitor):
            visitor.visit(self)
            self.visitors+= (visitor, )
        else:
            self.reject(visitor)
        return visitor

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
        self.accept_all(*visitors[-2::-1])

    def rollback(self, visitor):
        if visitor not in self.visitors: return
        index = self.visitors.index(visitor)
        return tuple(map(self.expunge, self.visitors[index:][::-1]))

    def expunge(self, visitor):
        if self.is_modifier(visitor):
            visitor.restore(self)
            self.remove_visitor(visitor)
        else:
            self.defer(visitor)
        return visitor

    def remove_visitor(self, visitor):
        if visitor in self.visitors:
            visitors = list(self.visitors)
            visitors.remove(visitor)
            self.visitors = tuple(visitors)

    @abstractmethod
    def defer(self, visitor):
        """What to do if visitor is not a Modifier"""
