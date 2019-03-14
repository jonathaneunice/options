"""
Tests of options method setting functions
"""

from options import Options
from options.methset import *
from pytest import raises


def test_methset():

    class Test(object):
        options = Options(this=1, that=1)

        def __init__(self, **kwargs):
            self.options = Test.options.push(kwargs)

        def something(self, **kwargs):
            opts = method_push(self.options, self.something.__kwdefaults__, kwargs)
            return opts.this + opts.that

        def another(self, **kwargs):
            opts = method_push(self.options, self.another.__kwdefaults__, kwargs)
            return opts.this + opts.that

    enable_func_set(Test.something, Test)
    enable_func_set(Test.another, Test)

    t = Test()
    assert t.options.this == 1
    assert t.options.that == 1

    assert t.something() == 2
    assert t.something(this=2) == 3
    assert t.something(that=2) == 3
    assert t.something(this=2, that=2) == 4

    t.something.set(this=10)
    assert t.something() == 11
    assert t.something(that=5) == 15

    assert t.another() == 2
    t.another.set(this=20)
    assert t.another() == 21
    assert t.another(this=10) == 11
    assert t.another() == 21

def test_methset_decorators():
    """
    Same tests as above, but with decorator-made class.
    """

    @enable_method_set
    class TestTwo(object):
        options = Options(this=1, that=1)

        def __init__(self, **kwargs):
            self.options = TestTwo.options.push(kwargs)

        @method_set
        def something(self, **kwargs):
            opts = method_push(self.options, self.something.__kwdefaults__, kwargs)
            return opts.this + opts.that

        @method_set
        def another(self, **kwargs):
            opts = method_push(self.options, self.another.__kwdefaults__, kwargs)
            return opts.this + opts.that

    t = TestTwo()
    assert t.options.this == 1
    assert t.options.that == 1

    assert t.something() == 2
    assert t.something(this=2) == 3
    assert t.something(that=2) == 3
    assert t.something(this=2, that=2) == 4

    t.something.set(this=10)
    assert t.something() == 11
    assert t.something(that=5) == 15

    assert t.another() == 2
    t.another.set(this=20)
    assert t.another() == 21
    assert t.another(this=10) == 11
    assert t.another() == 21






