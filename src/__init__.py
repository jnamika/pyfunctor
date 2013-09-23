# -*- coding:utf-8 -*-
'''
pyfunctor is a Python Functor library that provides classes implementing
lazy evaluation, pipeline operators and block syntax.

An example of usages is following:

    >>> from functor import *
    >>> f = (Functor(range(10)) >> c_(map)(lambda x: x * 2)
    ...      >> c_(filter)(lambda x: x < 7)
    ...      >> c_(sorted).key(lambda x: -x))
    >>> run(f)  # lazy evaluation
    [6, 4, 2, 0]

The 'Functor' class packs a value into a context.
The pipeline operator '>>' composes functions, but it is not calculated until
'run' function is applied to the Functor object.

Furthermore, Functor object will work together with the 'with' statement.
The object is only once evaluated after the with-block is done.

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
'''

__author__ = 'Jun Namikawa'
__email__ = 'jnamika@gmail.com'
__version__ = '0.1.1'
__license__ = 'ISC License (ISCL)'
