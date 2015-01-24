# -*- coding: utf8 -*-
from functools import partial
from . import stack

class Modifier(object):
    """Visitor with rollback"""
    def visit(self, visited):
        """do something on visited"""
        msg = "[method visit] %s can't visit %s" %(self, visited)
        raise NotImplementedError(msg)

    def visit_all(self, *visited):
        return tuple(map(self.visit, visited))

    def restore(self, visited):
        """restore visited state"""
        msg = "[method restore] %s can't restore %s" %(self, visited)
        raise NotImplementedError(msg)

    def restore_all(self, *visited):
        return tuple(map(self.restore, visited))

class modifier(Modifier):
    """
        decorator to construct modifier from function
        if restore not given the first call to restore set restore_func
    """
    def __init__(self, visit, restore=None):
        if not restore:
            restore = lambda visited: setattr(self, 'restore_func', visited)
        setattr(self, 'visit_func', visit)
        setattr(self, 'restore_func', restore)

    def visit(self, visited):
        return self.visit_func(visited)
    __call__ = visit

    def __eq__(self, other):
        if isinstance(other, type(self)):
            other = other.visit_func
        return other == self.visit_func

    def restore(self, visited):
        return self.restore_func(visited)


class RejectedModifier(Modifier):
    """Use a special Visitor for refuseed item to provide more information on errors"""
    def __init__(self, item, refuse_func, reject_func):
        self.item = item
        self.refuse = refuse_func
        self.reject = reject_func

    def visit(self, visited):
        return self.refuse(visited, self.item)

    def restore(self, visited):
        return self.reject(visited, self.item)

    def __eq__(self, other):
        return other == self.item

class Modifiers(Modifier, stack.Checked):
    """Visitors with rollback"""

    def __init__(self, items=[], refuse=None, reject=None):
        if callable(reject):
            self.reject = reject
        if callable(refuse):
            self.refuse = refuse
        stack.Checked.__init__(self, items)

    def check(self, item):
        return isinstance(item, Modifier)

    def fallback(self, item):
        return RejectedModifier(item, self.refuse, self.reject)

    def visit(self, visited):
        """accept visitors to visited"""
        return self.accept_all(visited, reversed(self))

    def restore(self, visited):
        return tuple(map(partial(self.deny, visited), self._items))

    def accept(self, visited, visitor):
        return visitor.visit(visited)

    def accept_all(self, visited, visitors):
        return tuple(map(partial(self.accept, visited), visitors))

    def deny(self, visited, visitor):
        return visitor.restore(visited)

    def append(self, visited, visitor):
        visitor = self.push(visitor)
        return self.accept(visited, visitor)

    def extend(self, visited, visitors):
        self.push_all(visitors)
        return self.accept_all(visited, visitors)

    def rollback(self, visited, visitor):
        return self.rollback_to(visited, self.index(visitor)+1)

    def rollback_to(self, visited, index):
        return tuple(self.consume(visited) for i in range(index))

    def consume(self, visited):
        return self.deny(visited, self.pop())

    def expunge(self, visited, visitor):
        index = self.index(visitor)
        items = self[:index]
        self.rollback_to(visited, index+1)
        return self.extend(visited, items)

    def refuse(self, visited, visitor):
        """What to do if visitor is not a Visitor when visit"""
        msg = "[method refuse] %s can't visit %s and be properly refused" % (visitor, visited)
        raise NotImplementedError(msg)

    def reject(self, visited, visitor):
        """What to do if visitor is not a Modifier when restore"""
        msg = "[method reject] %s can't restore %s and be properly rejectred" % (visitor, visited)
        raise NotImplementedError(msg)
