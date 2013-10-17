# -*- coding:utf-8 -*-

import sys
import types
from functools import reduce
from itertools import chain
from operator import itemgetter


class Functor:
    '''Functor(value) -> new Functor object

    Alias for Functor: F

    Example 1 (pipeline operator):
    >>> x = Functor('abc')
    >>> y = x >> str.upper >> (lambda x: x + 'def')
    >>> run(y)
    'ABCdef'

    Example 2 (with block):
    >>> with Functor(0):
    ...     def f(x):
    ...         return x + 10
    ...     def b(x):
    ...         return x * 2
    ...     def c(x):
    ...         print(x)
    20
    '''
    def __init__(self, x):
        self.value = x
        self.fs = []

    @classmethod
    def fmap(cls, f):
        return f

    @classmethod
    def lift(cls, f):
        def _f(*margs):
            args = (m.run() for m in margs)
            return cls.fmap(f)(*args)
        return _f

    def run(self):
        '''F.run() -> calcuated value'''
        return reduce(lambda x, f: f(x), self.fs, self.value)

    def _composition(self, f):
        functor = self.__class__(self.value)
        functor.fs = self.fs + [self.fmap(f)]
        return functor

    def __rshift__(self, f):
        return self._composition(f)

    def __rlshift__(self, f):
        return self._composition(f)

    def __call__(self):
        return self.run()

    def __eq__(self, x):
        return (self.__class__ == x.__class__ and self.fs == x.fs and
                self.value == x.value)

    def __enter__(self):
        def call(self, f):
            def _(*args, **kwd):
                return f(*args, **kwd)
            _._src_location = _location(1)[:2]
            self._slots.append(_)
            return _
        self._start = _location(1)[1]
        self._functor = self.__class__(None)
        self._functor._slots = []
        self._functor.call = types.MethodType(call, self._functor)
        return self._functor

    def __exit__(self, extype, exval, tb):
        if extype is None:
            filename, end, f_locals = _location(1)
            fs = set()
            for f in chain(f_locals.values(), self._functor._slots):
                if isinstance(f, types.FunctionType):
                    if hasattr(f, '_src_location'):
                        fn, n = f._src_location
                    else:
                        code = f.__code__
                        fn, n = code.co_filename, code.co_firstlineno
                    if fn == filename and self._start <= n <= end:
                        fs.add((n, f))
            functor = self
            for n, f in sorted(fs, key=itemgetter(0)):
                functor = functor._composition(f)
            self._functor.value = functor.run()
        return False

F = Functor


def run(x):
    '''run(functor) -> calcuated value'''
    return x.run()


class Lift:
    '''Lift(func) -> new function lifted into a functor's context.

    Alias for Lift: lift

    Example:
    >>> x = (lambda x: x + 1) << F(3)
    >>> y = (lambda x: x ** 2) << F(5)
    >>> z = lift(lambda x, y: x + y)(x, y)
    >>> z()
    29'''
    def __init__(self, f):
        self.f = f

    def __call__(self, *margs):
        cls = margs[0].__class__
        _f = lambda _: cls.lift(self.f)(*margs)
        functor = cls(None)
        functor.fs.append(_f)
        return functor

lift = Lift


def _location(depth=0):
    frame = sys._getframe(depth + 1)
    return frame.f_code.co_filename, frame.f_lineno, frame.f_locals


class Curry:
    '''Curry(func) -> new curried function.
    Curry(func, n) -> new curried function with an argument index.
    Curry(func).name -> new curried function with a keyword argument.
    Curry(func, keyword='name') -> it is same as Curry(func).name

    This converts an uncurried function to a curried function.

    Alias for Curry: curry, c_

    The following laws are satisfied:
    c_(f)(x)(*args, **kwd) == f(x, *args, **kwd)
    c_(f, n)(x)(*args, **kwd) == f(*(list(args[:n])+[x]+list(args[n:])), **kwd)
    c_(f).name(x)(*args, **kwd) == f(*args, **dict(name=x, **kwd)))
    c_(f, keyword='name')(x)(*args, **kwd) == f(*args, **dict(name=x, **kwd)))

    Example 1:
    >>> run(F(range(10)) >> c_(map)(lambda x: x * 2)
    ...                  >> c_(filter)(lambda x: x < 7)
    ...                  >> c_(sorted).key(lambda x: -x))
    [6, 4, 2, 0]

    Example 2 (decorator):
    >>> with F(range(10)) as box:
    ...     @c_(map)
    ...     def f(x):
    ...         y = x % 3
    ...         z = x + y
    ...         return x + y + z
    ...     @c_(sorted, keyword='key')
    ...     def g(x):
    ...         return (x % 7, x % 3, x)
    >>> box.value
    [0, 14, 8, 16, 10, 18, 4, 12, 6, 20]
    '''
    def __init__(self, func, index=0, keyword=None):
        self._func = func
        self._argument_index = index
        self._keyword_argument = keyword

    def __call__(self, x):
        def _(*args, **kwd):
            if self._keyword_argument is None:
                args = list(args)
                args.insert(self._argument_index, x)
            else:
                kwd = kwd.copy()
                kwd[self._keyword_argument] = x
            return self._func(*args, **kwd)
        _._src_location = _location(1)[:2]
        return _

    def __getattr__(self, keyword):
        self._keyword_argument = keyword
        return self

curry = Curry
c_ = Curry


def call(f):
    def _(*args, **kwd):
        return f(*args, **kwd)
    _._src_location = _location(1)[:2]
    return _
