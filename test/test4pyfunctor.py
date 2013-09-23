# -*- coding:utf-8 -*-

from functor import Functor, c_
from list import ListF
import unittest


class TestFunctor(unittest.TestCase):
    def test_functor_law(self):
        x = 10
        f1 = Functor(x) >> (lambda x: x)
        self.assertEqual(f1(), x)
        add1 = lambda x: x + 1
        f2 = Functor(x) >> add1 >> str
        f3 = Functor(str(add1(x)))
        self.assertEqual(f2(), f3())

    def test_with(self):
        with Functor('abc') as r:
            def f(x):
                return x.upper()
            def g(x):
                return x + 'def'
        self.assertEqual(r.value, 'ABCdef')

    def test_curry(self):
        f = Functor(range(10)) >> c_(map)(lambda x: x + 1)
        f = f >> c_(sorted).key(lambda x: (x % 3, x))
        expected_value = sorted(range(1, 11), key=lambda x: (x % 3, x))
        self.assertEqual(f(), expected_value)
        with Functor(range(10)) as r:
            @c_(map)
            def f(x):
                return x + 1
            @c_(sorted, keyword='key')
            def g(x):
                return (x % 3, x)
        self.assertEqual(r.value, expected_value)

    def test_call(self):
        with Functor('abc') as r:
            r.call(str.upper)
            r.call(lambda x: x + 'def')
        self.assertEqual(r.value, 'ABCdef')
        deco = lambda f: (lambda x: f(x))
        with Functor('abc') as r:
            @r.call
            @deco
            def f(x):
                return x + 'def'
            r.call(str.upper)
            def g(x):
                return 'z' + x
        self.assertEqual(r.value, 'zABCDEF')


class TestListF(unittest.TestCase):
    def test_functor_law(self):
        xs = list(range(10))
        f1 = ListF(xs) >> (lambda x: x)
        self.assertEqual(f1(), xs)
        add1 = lambda x: x + 1
        f2 = ListF(xs) >> add1 >> str
        f3 = ListF([str(add1(x)) for x in xs])
        self.assertEqual(f2(), f3())

if __name__ == '__main__':
    unittest.main()
