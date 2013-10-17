# -*- coding:utf-8 -*-

from itertools import product
from pyfunctor.functor import Functor


class ListF(Functor):
    '''ListF(value) -> new Functor object for lists

    Alias for ListF: L

    Example:
    >>> run(L([1, 2, 3]) >> (lambda x: x + 1))
    [2, 3, 4]
    >>> f = lift(lambda x, y: (x, y))
    >>> run(f(L(range(3)), L('ab')))
    [(0, 'a'), (0, 'b'), (1, 'a'), (1, 'b'), (2, 'a'), (2, 'b')]
    '''
    def run(self):
        '''L.run() -> calcuated value'''
        return list(Functor.run(self))

    @classmethod
    def fmap(cls, f):
        def _f(*args):
            # itertools.product is only used when getting multiple arguments
            # because itertools.product evaluates eagerly.
            if len(args) == 1:
                return (f(x) for x in args[0])
            else:
                return (f(*x) for x in product(*args))
        return _f

    @classmethod
    def lift(cls, f):
        def _f(*margs):
            args = (Functor.run(m) for m in margs)
            return cls.fmap(f)(*args)
        return _f

    def __iter__(self):
        return Functor.run(self)

L = ListF
