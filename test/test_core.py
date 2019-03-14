"""
Tests of options core functions
See test_use.py for more applied testing
"""

from options import *
import sys, six, pytest, platform, os
from pytest import raises

def test_good_chainstuf():
    """
    Test options class for being faithful subclass of chainstuf
    """

    # make some base dictsw
    d1 = Options(this=1, that=2, roger=None)
    d2 = dict(roger=99, that=100)

    # test simple attribute equivalence
    dd = d1.push(d2)
    assert dd.this == 1
    assert dd.roger == 99
    assert dd.this == dd['this']
    assert dd.that == dd['that']

    assert dd.roger == dd['roger']

    # set value, ensure properly set, in top dict
    dd.roger = 'wilco'
    assert dd.roger == 'wilco'


def test_eq():
    o1 = Options(a=1, b=3, c=9)
    o2 = Options(a=1, b=3, c=9)
    assert o1 is not o2
    assert o1 == o2

    o3 = Options(a=1, b=3, c=102)
    assert o1 != o3
    assert o2 != o3
    o3a = o3.push({})
    assert o3 == o3a

    del o1.maps[0]['b']
    assert o1 != o2

    o1a = o1.add(b=3)
    assert o1a == o2


def test_repr():
    o = Options(a=1, b=3)
    oo = o.push({'a':12})
    assert repr(oo) in [ 'Options(a=12, b=3)', 'Options(b=3, a=12)' ]


def test_setdefault():
    o = Options(ok=1, prohib=Prohibited, none=None,
                trans=Transient, unset=Unset)

    oo = o.add(another='other stuff')

    # regular set value
    assert o.setdefault('ok', 2) == 1
    assert o.ok == 1

    # regular set value
    assert 'unknown' not in o
    with raises(KeyError):
        o.setdefault('unknown', 2)

    # None value
    assert o.setdefault('none', 44) is None
    assert o.none is None

    # Unset value
    assert o.setdefault('unset', 33) == 33
    assert o.unset == 33

    # Transient value
    assert oo.trans is Transient
    assert oo.setdefault('trans', 100) == 100
    assert oo.trans == 100
    oo['trans'] = Transient

    assert o.setdefault('trans', -99) == -99
    assert o.trans == -99


    # Prohibited value
    with raises(KeyError):
        o.setdefault('prohib', 15)
    assert o.prohib is Prohibited

    oo = o.push({'a': 'first letter'})

    # regular set value
    assert oo.setdefault('ok', 2) == 1
    assert oo.ok == 1

    # regular set value
    assert 'unknown' not in o
    with raises(KeyError):
        oo.setdefault('unknown', 2)

    # None value
    assert oo.setdefault('none', 44) is None
    assert oo.none is None

    # Unset value
    assert oo.setdefault('unset', 33) == 33
    assert oo.unset == 33

    # Transient value
    assert oo.setdefault('trans', -99) == -99
    assert oo.trans == -99

    # Prohibited value
    with raises(KeyError):
        oo.setdefault('prohib', 15)
    assert oo.prohib is Prohibited


def test_prohibited():
    d1 = Options(this=1, that=2, roger=None, fish=Prohibited)
    dd = d1.push(dict(roger=99, that=100))

    with pytest.raises(KeyError):
        dd.set(fish='in pan')


def test_unset():
    d1 = Options(this=1, that=2, roger=None, fish='swim')
    dd = d1.push(dict(roger=99, that=100))
    de = dd.push(dict(fish='wanda', that='fish'))

    assert de.that == 'fish'

    de.set(that=Unset)
    assert de.that == 100

    de.set(that='fishy')
    assert de.that == 'fishy'

    de.set(that=Unset)
    assert de.that == 100

    assert dd.that == 100
    dd.set(that=Unset)

    assert dd.that == 2
    assert de.that == 2

def test_magic():

    o = Options(this=1, slick='slack', blik=99)
    o['_magic'] = { 'slick': lambda x: x.capitalize() }

    # test that magic doesnt effect everything
    o.blik = "wubber"
    assert o.blik == 'wubber'

    # test that it does effect the right things
    o.set(slick='mack')
    assert o.slick == 'Mack'  # note magical capitalization

    p = o.push(dict(this=2))
    assert p.this == 2
    assert p.slick == 'Mack'


def test_magic_designation():

    class T(object):
        options = Options(
            this=1,
            slick='slack',
            nick='nack',
            blik=99,
            man='man'
        )

        # technique 1: lambda expression or function
        options.magic(
            slick = lambda v: v.capitalize(),
        )

        def __init__(self, *args, **kwargs):
            self.options = T.options.push(kwargs)
            self.data = args

        def set(self, **kwargs):
            """
            Uplevel the set operation. A set() on this object is converted into
            a set on its options.
            """
            self.options.set(**kwargs)

        # technique 2 - a static method with after-the-fact inclusion

        @staticmethod
        def nick_magic(v, cur):
            return v.upper()

        options.magic(nick=nick_magic)

        # technique 3 - a decorated method

        @options.magical('man')
        def man_magic(self, v, cur):
            return v.upper()

    t = T()
    assert t.options.this == 1
    assert t.options.blik == 99
    assert t.options.nick == 'nack'
    assert t.options.slick == 'slack'
    t.set(slick='slack')
    assert t.options.slick == 'Slack'
    t.set(slick='wack')
    assert t.options.slick =='Wack'
    t.set(nick='flick')
    assert t.options.nick == 'FLICK'

    t.set(man='boy')
    assert t.options.man == 'BOY'
    t.set(man='girl')
    assert t.options.man == 'GIRL'


def test_len():
    o = Options()
    assert len(o) == 1  # _magic element

    o = Options(a=1)
    assert len(o) == 2

    o = Options(a=1, b=4, c=11)
    assert len(o) == 4

    # should _magic be a genuine property? or present only when needed?


def test_push():

    class T2(object):
        options = Options(
            this=1,
            slick='slack',
            nick='nack',
            blik=99,
            man='man'
        )

        def __init__(self, *args, **kwargs):
            self.options = T2.options.push(kwargs)
            self.data = args

        def set(self, **kwargs):
            """
            Uplevel the set operation. A set() on this object is converted into
            a set on its options.
            """
            self.options.set(**kwargs)

        def write(self, **kwargs):
            opts = self.options.push(kwargs)
            six.print_(opts.nick)

        def push1(self, **kwargs):
            opts = self.options.push(kwargs)

            # persistent data test
            assert T2.options.nick == 'nack'
            assert T2.options.slick == 'slack'
            assert t.options.nick == 'N'
            assert t.options.slick == 'S'

            # transient data test
            assert opts.nick == 44
            assert opts.slick == 55

    t = T2(nick='N', slick='S')
    assert T2.options.nick == 'nack'
    assert T2.options.slick == 'slack'
    assert t.options.nick == 'N'
    assert t.options.slick == 'S'
    t.push1(nick=44, slick=55)

    T2.options._magic['nick'] = lambda x, y, z, plus: 42
    with pytest.raises(ValueError):
        t.options.set(nick='something')


def test_push_takes():
    """
    Ensure that push sets the values property, but even
    more so, that it leaves the proper leftovers.
    """
    o = Options(a=1, b=4, c=4)
    d = dict(a=11, b=44)
    oo = o.push(d)

    assert o.a == 1
    assert o.b == 4
    assert o.c == 4
    assert len(o) == 4 # consider _magic key as well

    assert oo.a == 11
    assert oo.b == 44
    assert oo.c == 4
    assert len(oo) == 4

    assert d == {}

    # round 2 -- ensure proper leftovers
    o = Options(a=1, b=4, c=4)
    d = dict(a=11, b=44, e=100)
    oo = o.push(d)
    assert d == {'e': 100}


def test_add():

    class T2(object):
        options = Options(
            this=1,
            slick='slack',
            nick='nack',
            blik=99,
            man='man'
        )

        def __init__(self, *args, **kwargs):
            self.options = T2.options.push(kwargs)
            self.data = args

    class T3(T2):

        options = T2.options.add(
            this = 99,
            man = 'Biff',
            rocker = 'Prince'
        )

        def __init__(self, *args, **kwargs):
            self.options = T3.options.push(kwargs)
            self.data = args

    t = T2(nick='N', slick='S')
    assert T2.options.nick == 'nack'
    assert T2.options.slick == 'slack'
    assert t.options.nick == 'N'
    assert t.options.slick == 'S'

    u = T3()
    assert u.options.nick == 'nack'
    assert u.options.slick == 'slack'
    assert u.options.this == 99
    assert u.options.man == 'Biff'
    assert u.options.rocker == 'Prince'


def test_update():

    options = Options(
        this=1,
        slick='slack',
        nick='nack',
        blik=99,
        man='man'
    )

    options2 = options.add(
        this = 99,
        man = 'Biff',
        rocker = 'Prince'
    )

    # base level values - assure they're right
    assert options2.nick == 'nack'
    assert options2.slick == 'slack'
    assert options2.this == 99
    assert options2.man == 'Biff'
    assert options2.rocker == 'Prince'

    # update base via list of tuples
    options.update([('nick', 'Danger'), ('man', 'more than a')])
    assert options.nick == 'Danger'
    assert options.man == 'more than a'

    assert options2.nick == 'Danger'
    assert options2.slick == 'slack'
    assert options2.this == 99
    assert options2.man == 'Biff'
    assert options2.rocker == 'Prince'

    # update base via dict
    options.update({'nick': 'olas'})
    assert options.nick == 'olas'
    assert options2.nick == 'olas'

    # update base via kwargs
    options.update(nick='flick', this=101)
    assert options.nick == 'flick'
    assert options.this == 101

    assert options2.nick == 'flick'
    assert options2.slick == 'slack'
    assert options2.this == 99
    assert options2.man == 'Biff'
    assert options2.rocker == 'Prince'

    # update layer 2 via list of tuples
    options2.update([('nick', 'Nolte')])
    assert options.nick == 'flick'
    assert options2.nick == 'Nolte'

    # update layer 2 via dict
    options2.update({'nick': 'at night'})
    assert options.nick == 'flick'
    assert options2.nick == 'at night'

    # update layer 2 via kwargs
    options2.update(nick='now tired')
    assert options.nick == 'flick'
    assert options2.nick == 'now tired'


def test_dictify():

    o = Options(
            this=1,
            slick='slack',
            nick='nack',
            blik=99,
            _special=12,
        )
    d = dict(o.items())
    assert not [ k for k in d.keys() if k.startswith('_') ]  # _values hidden
    assert o.this == d['this'] == 1

    oo = o.push(dict(this=99, _grim='grey'))
    dd = dict(oo.items())
    assert not [ k for k in dd.keys() if k.startswith('_') ]  # _values hidden
    assert oo.this == dd['this'] == 99

    # Wish we could just do ``dict(o)`` without passing through ``items()``. But how?

def test_files():
    # The underlying stuf container used to have (<0.9.9) a problem with files
    # being assigned in a stuf() constructor. This tests that we're over that
    # problem.

    # Get names of files that won't be munged by py.test's capturing mechanism
    # (sys.stdout and sys.stderr definitely will be overtaken by py.test, but
    # their primitive double-underscore names won't be). This doesn't seem to
    # be an issue with Python 2.x, but spuriously screws up the test otherwise
    # in Python 3.x (gives false negative, saying module not working when it is)

    f1 = sys.__stdout__
    f2 = sys.__stderr__
    f3 = sys.__stdin__

    o = Options(a=f1, b=f2, c=[f2, f3])

    assert o.a is f1
    assert o.b is f2
    assert len(o.c) == 2
    assert o.c[0] is f2
    assert o.c[1] is f3

    # first push
    oo = o.push(dict(b=f1, c=12))
    assert oo.a is f1
    assert oo.b is f1
    assert oo.c == 12

    # second push
    ooo = oo.push(dict(a=f2, b=f3))
    assert ooo.a is f2
    assert ooo.b is f3
    assert ooo.c == 12

    # partial unset
    ooo.set(a=Unset)
    assert ooo.a is f1
    assert ooo.b is f3
    assert ooo.c == 12

    # Test fails under PyPy.

def test_generators():
    # Stuf seems to have trouble sometimes with generators being assigned
    # in update operations. Options and OptionChain implement update
    # themselves as a workaround. This test confirms the workaround works.

    import types

    def gen():
        n = 1
        while True:
            yield n
            n += 1

    _PY3 = sys.version_info[0] == 3

    def next(g):
       return g.__next__() if _PY3 else g.next()

    g = gen()

    o = Options(a=1, b=2, gen=gen, g=g)
    assert type(o.g) == types.GeneratorType
    assert next(o.g) == 1
    assert next(o.g) == 2
    o.g = g
    assert next(o.g) == 3
    o.update(g=g)
    assert next(o.g) == 4
    o.update({'g': g})
    assert next(o.g) == 5

    oo = o.push({})
    assert next(oo.g) == 6


def test_addflat():
    class AF(object):
        options = Options(
            prefix = None,
            suffix = None
        )

        def __init__(self, *args, **kwargs):
            self.options = AF.options.push(kwargs)
            if args:
                used = self.options.addflat(args, ['prefix', 'suffix'])
                if 'suffix' not in used:
                    self.options.suffix = self.options.prefix
            else:
                # nonsense in general, but helps test case if no args given
                used = self.options.addflat(args, ['prefix', 'suffix'])


    a = AF(prefix='[', suffix=']')
    assert a.options.prefix == '['
    assert a.options.suffix == ']'

    b = AF('|')
    assert b.options.prefix == '|' == b.options.suffix

    c = AF('{', '}')
    assert c.options.prefix == '{'
    assert c.options.suffix == '}'

    d = AF()

    with pytest.raises(ValueError):
        d = AF('a', 'b', 'c')  # too many values!

def test_copy():
    options = Options(
            this=1,
            slick='slack',
            nick='nack',
            blik=99,
            man='man'
        )
    o1 = options.copy()
    assert o1 is not options
    assert o1 == options

    o2 = options.push(dict(this=4, blik='rubber'))
    assert o2.nick == 'nack'
    assert o2.slick == 'slack'
    assert o2.blik  == 'rubber'
    assert o2.this  == 4

    # now make a copy - check data is the same
    o3 = o2.copy()
    assert o3 is not o2
    assert o3.nick == 'nack'
    assert o3.slick == 'slack'
    assert o3.blik  == 'rubber'
    assert o3.this  == 4

    # make sure copy is not using sam
    o2.slick = 999
    assert o2.slick == 999
    assert o3.slick == 'slack'

def test_no_aliases():
    # o works just fine
    o = Options(color='red', shape='box')
    assert o.color == 'red'
    assert o.shape == 'box'

    # but not if you try to add a bad option to it
    with raises(BadOptionName):
        o.add(items=55)
        assert False

    # cant create it initially wiht bad option name, either
    with raises(BadOptionName):
        o = Options(color='red', shape='box', items=False)
        assert False

    # o and oo are fine, but cant add bad option to it either
    o = Options(color='red', shape='box')
    oo = o.push({})
    with raises(BadOptionName):
        ooo = oo.add(values=44)
        assert False
