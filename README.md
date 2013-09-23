pyfunctor: A Functor library for Python (with lazy evaluation, pipeline operators and block syntax)

Copyright (c) 2013, Jun Namikawa <jnamika@gmail.com>
License: ISC License (ISCL)



pyfunctor is a Python Functor library that provides classes implementing lazy evaluation, pipeline operators and block syntax.

An example of usages is following:

    >>> from pyfunctor.functor import *
    >>> f = Functor(range(10)) >> c_(map)(lambda x: x * 2)
    ...                        >> c_(filter)(lambda x: x < 7)
    ...                        >> c_(sorted).key(lambda x: -x)  # the pipeline operator '>>' composes functions
    >>> run(f)  # lazy evaluation
    [6, 4, 2, 0]

Furthermore, Functor object will work together with the 'with' statement.
The object is only once evaluated after the with-block is done.

    >>> with Functor(range(10)) as box:
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




pyfunctorチュートリアル

はじめに:
pyfunctorはPython用のFunctorライブラリです。遅延評価、パイプライン演算子、with構文を利用したブロックをサポートしています。


(1)
クラスFunctor（別名F）のインスタンスで値をラップする（以下ではFunctor値と呼びます）ことで、値をFunctorのコンテクストに持ち上げることができます。
Functor値に対してはパイプライン演算子>>で関数を連結することができます。
関数を連結するだけでは計算は実行されません（遅延評価）。
run関数をFunctor値に適用することで、はじめて計算が実行されます（Functor値のメソッドrunを呼び出す、Functor値を関数として実行する、などでも同様の結果が得られます）。

    >>> x = F('abc')
    >>> y = x >> str.upper >> (lambda x: x + 'def')
    >>> run(y)
    'ABCdef'
    >>> y.run()
    'ABCdef'
    >>> y()
    'ABCdef'



(2)
liftで関数を持ち上げる事で、Functor値を引数に取る事ができるようになります。
複数のFunctor値を使って一つの計算を作る事ができます。

    >>> x = F(3) >> (lambda x: x + 1)
    >>> y = F(5) >> (lambda x: x ** 2)
    >>> z = lift(lambda x, y: x + y)(x, y)
    >>> z()
    29



(3)
逆向きのパイプライン演算子<<も存在します。

    >>> run(len << F('abcde'))
    5



(4)
遅延評価が不要な場合はwith構文を使う事ができます。
withブロックの中で定義された関数が順番にFunctor値に適用され、withブロックを抜けた時点で即座に（一度だけ）実行されます。

    >>> with F(0):
    ...     def f(x):
    ...         return x + 10
    ...     def b(x):
    ...         return x * 2
    ...     def c(x):
    ...         print(x)
    20



(5)
with構文で生成されたインスタンス(with * as varname の varname）に実行結果の戻り値が格納されます。
戻り値を格納したインスタンスはFunctor値なので、再び関数を連結することができます。

    >>> with F(123) as box:
    ...     def f(x):
    ...         return x % 7
    ...     def b(x):
    ...         return x * 2
    ...
    >>> box.value
    8
    >>> run(box >> (lambda x: x * 2))
    16



(6)
リスト等に対する処理をサポートするため、部分適用を補助する関数c_が存在します。
次の処理は sorted(filter(lambda x: x < 7, map(lambda x: x * 2, range(10))), key=lambda x: -x) と同等です。

    >>> run(F(range(10)) >> c_(map)(lambda x: x * 2)
    ...                  >> c_(filter)(lambda x: x < 7)
    ...                  >> c_(sorted).key(lambda x: -x))
    [6, 4, 2, 0]

また、c_をデコレータとして使用することもできます。

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



(7)
with構文の中で定義済みの関数を連結する場合にはcallメソッドを使います。

    >>> with F('abc') as box:
    ...     box.call(str.upper)
    ...     box.call(lambda x: x + 'def')
    >>> box.value
    'ABCdef'



(8)
Functorクラスはデフォルトの挙動としてIdentityを実装しています。
しかし、Functor則を満たすものならばFunctorクラスを継承して実装できます。
一例としてリストのFunctorを実装したpyfunctor.list.ListF（別名L）が提供されています。

    >>> run(L([1, 2, 3]) >> (lambda x: x + 1))
    [2, 3, 4]
    >>> f = lift(lambda x, y: (x, y))
    >>> run(f(L(range(3)), L('ab')))
    [(0, 'a'), (0, 'b'), (1, 'a'), (1, 'b'), (2, 'a'), (2, 'b')]
