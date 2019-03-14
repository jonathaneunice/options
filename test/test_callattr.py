
from options.callattr import *


def run_through_paces(target):
    assert not callable_hasattr(target, 'bozo')
    assert callable_getattr(target, 'bozo') is None

    callable_setattr(target, 'bozo', 12)
    assert callable_hasattr(target, 'bozo')
    assert callable_getattr(target, 'bozo') == 12

    callable_setattr(target, 'bozo', 13)
    assert callable_hasattr(target, 'bozo')
    assert callable_getattr(target, 'bozo') == 13


def test_function():

    def f(a, b):
        return a + b

    run_through_paces(f)


def test_method_explict_superclass():

    class O(object):
        def m(self):
            return 12

    run_through_paces(O.m)


def test_method_implicit_superclass():

    class O:
        def m(self):
            return 12

    run_through_paces(O.m)


def test_callable_instance():

    class C(object):
        def __call__(self):
            return 12

    c = C()
    assert c() == 12

    run_through_paces(c)


def test_lambda():

    f = lambda: 12
    assert f() == 12

    run_through_paces(f)
