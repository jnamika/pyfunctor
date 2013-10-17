# -*- coding:utf-8 -*-

from functools import reduce
from pyfunctor.functor import Functor


class Maybe(Functor):
    '''Maybe(value) -> new Functor object

    Example:
    >>> f = lift(lambda x, y: x + y)
    >>> run(f(Just('a'), Just('b')))
    Just('ab')
    >>> run(f(Just(0), Nothing))
    Nothing
    '''
    def run(self):
        return reduce(lambda x, f: f(x), self.fs, self)

    @classmethod
    def fmap(cls, f):
        def _f(*args):
            try:
                if all(isinstance(x, Just) for x in args):
                    return Just(f(*(x.value for x in args)))
                else:
                    return Nothing
            except:
                return Nothing
        return _f


class Just(Maybe):
    def __str__(self):
        if self.fs == []:
            x = self.value
            s = "'%s'" % x if isinstance(x, str) else x
            return 'Just(%s)' % s
        else:
            return 'Maybe(?)'

    def __repr__(self):
        if self.fs == []:
            return self.__str__()
        else:
            return '<%s>' % self.__str__()

class Nothing(Maybe):
    def __str__(self):
        return 'Nothing'

    def __repr__(self):
        return self.__str__()


Nothing = Nothing(None)
