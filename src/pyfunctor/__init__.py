# -*- coding:utf-8 -*-
'''
pyfunctor is a Python Functor library that provides classes implementing
lazy evaluation, pipeline operators and block syntax.

An example of usages is following:

    >>> from pyfunctor.functor import *
    >>> f = (Functor(range(10)) >> c_(map)(lambda x: x * 2)
    ...      >> c_(filter)(lambda x: x < 7)
    ...      >> c_(sorted).key(lambda x: -x))
    >>> run(f)  # lazy evaluation
    [6, 4, 2, 0]

The 'Functor' class packs a value into a context.
The pipeline operator '>>' composes functions, but it is not calculated until
'run' function is applied to the 'Functor' instance.

Furthermore, 'Functor' instance will work together with the 'with' statement.
The instance is only once evaluated after the with-block is done.

    >>> with Functor(range(10)) as box:
    ...     @c_(map)
    ...     def f(x):
    ...         y = x % 3
    ...         z = x + y
    ...         return x + y + z
    ...
    ...     @c_(sorted, keyword='key')
    ...     def g(x):
    ...         return (x % 7, x % 3, x)
    >>> box.value
    [0, 14, 8, 16, 10, 18, 4, 12, 6, 20]

In general, functors are things that can be mapped over, like Lists, Maybes and such.
The 'Functor' class implements the identity functor to provide a default implementation.
As other examples, 'ListF' and 'Maybe' are provided.

    >>> from pyfunctor.list import *
    >>> run(ListF([1, 2, 3]) >> (lambda x: x + 1))
    [2, 3, 4]
    >>> f = lift(lambda x, y: (x, y))
    >>> run(f(ListF(range(3)), ListF('ab')))
    [(0, 'a'), (0, 'b'), (1, 'a'), (1, 'b'), (2, 'a'), (2, 'b')]

    >>> from pyfunctor.maybe import *
    >>> @lift
    ... def func(x):
    ...     if x > 0: return x * 2
    ...     else: raise Exception()
    >>> func(Just(1)).run()
    Just(2)
    >>> func(Just(0)).run()
    Nothing
'''

__author__ = 'Jun Namikawa'
__email__ = 'jnamika@gmail.com'
__version__ = '0.1.3'
__license__ = 'ISC License (ISCL)'
