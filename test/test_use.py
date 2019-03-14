"""
Tests of using options
"""


from options import *
import sys, six, pytest, platform, os
from pytest import raises

def dicty(s):
    """
    Test helper. Helps test dict equivalence. Given different versions of Python,
    stringified dicts may have different item order. This gets us back to real
    dicts, which have more logical equality operations.
    """
    d = eval('dict({0})'.format(s))
    if '_magic' in d:
        del d['_magic']
    return d

def test_docs_example():

    class Shape(object):

        options = Options(
            name   = None,
            color  = 'white',
            height = 10,
            width  = 10,
        )

        def __init__(self, **kwargs):
            self.options = Shape.options.push(kwargs)

        def draw(self, **kwargs):
            opts = self.options.push(kwargs)
            # in this case, return actual, simplified dict, not string
            # (docs shows string return)
            d = dict(opts)
            if '_magic' in d:
                del d['_magic']
            return d

        def settings(self, **kwargs):
            return ShapeContext(self, kwargs)

    class ShapeContext(OptionsContext):
        pass

    one = Shape(name='one')
    assert one.draw() == dicty("color='white', width=10, name='one', height=10")
    assert one.draw(color='red') == dicty("color='red', width=10, name='one', height=10")
    assert one.draw(color='green', width=22) == dicty("color='green', width=22, name='one', height=10")

    Shape.options.set(color='blue')
    assert one.draw() == dicty("color='blue', width=10, name='one', height=10")
    one.options.set(color='red')
    assert one.draw(height=100) == dicty("color='red', width=10, name='one', height=100")
    assert one.draw(height=44, color='yellow') == dicty("color='yellow', width=10, name='one', height=44")


    def is_tall(self, **kwargs):
        opts = self.options.push(kwargs)
        return opts.height > 100

    assert not is_tall(one)

    with one.settings(height=200, color='purple'):
        assert one.draw() == dicty("color='purple', width=10, name='one', height=200")
        assert is_tall(one)

    assert not is_tall(one)

    # not in docs, but simple extension

    with one.settings(height=200, color='purple', opts={'width': 14}):
        assert one.draw() == dicty("color='purple', width=14, name='one', height=200")
        assert is_tall(one)
    assert not is_tall(one)


def test_OptionsClass_repr():
    class R(OptionsClass):
        pass

    class S(OptionsClass):
        options = Options(a=1)

    r = R()
    s = S()

    assert repr(r) == "R()"
    assert repr(s) == "S(a=1)"


def test_OptionsClass_set():
    class S(OptionsClass):
        options = Options(a=1)

    s = S()
    assert s.options.a == 1
    s.set(a=12)
    assert s.options.a == 12


def test_OptionsClass_settings():
    class S(OptionsClass):
        options = Options(a=1)

    s = S()
    assert s.options.a == 1

    with s.settings(a=99):
        assert s.options.a == 99

    assert s.options.a == 1


def test_read_write(tmpdir):
    tname1 = str(tmpdir.join("test1.json"))
    tname2 = str(tmpdir.join("test2.json"))

    o = Options(color='red', shape='box')
    o.write(tname1)
    ro = Options.read(tname1)
    assert o == ro
    assert sorted(o.keys()) == sorted(ro.keys())

    o2 = o.add(color='blue')
    o2.write(tname2)
    ro2 = Options.read(tname2)
    assert o2 == ro2
    assert sorted(o2.keys()) == sorted(ro2.keys())

