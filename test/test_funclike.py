
from options.funclike import *
import pytest

### Setup

def f():
    pass

class C(object):

    def __init__(self, v):
        self.v = v

    @staticmethod
    def f(x):
        return x * x

    @staticmethod
    def f4(x, a, b, c):
        return x + a + b + c

    def m(self, x):
        return x


c = C(12)

### Tests


def test_function_type():
    assert type(f) is function_type


def test_is_function():
    assert is_function(f)
    assert is_function(lambda: False)
    assert not is_function(4)
    assert not is_function("lsdjflkj")
    assert not is_function([1,2,3])


def test_real_func():
    assert real_func(f) is f
    assert is_function(real_func(f))
    assert is_function(real_func(C.f))
    assert is_function(real_func(c.f))
    assert is_function(real_func(C.f4))
    assert is_function(real_func(c.f4))

    # what happens if it's not a function?
    with pytest.raises(ValueError):
        real_func(44)


def test_func_code():
    assert hasattr(func_code(f), 'co_argcount')
    assert hasattr(func_code(C.f), 'co_argcount')
    assert hasattr(func_code(c.f), 'co_argcount')
    assert func_code(f).co_argcount == 0
    assert func_code(C.f).co_argcount == 1
    assert func_code(c.f).co_argcount == 1
    assert func_code(c.f4).co_argcount == 4

    # what happens if it's not a function?
    with pytest.raises(ValueError):
        func_code(44)
