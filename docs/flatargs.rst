Flat Arguments
==============

Sometimes it's more elegant to provide some arguments as flat, sequential values
rather than by keyword. In this case, use the ``addflat()`` method::

    def __init__(self, *args, **kwargs):
        self.options = Quoter.options.push(kwargs)
        self.options.addflat(args, ['prefix', 'suffix'])

to consume optional ``prefix`` and ``suffix`` flat arguments. This makes the following
equivalent::

    q1 = Quoter('[', ']')
    q2 = Quoter(prefix='[', suffix=']')

An explicit ``addflat()`` method is provided not as much for Zen of Python
reasons ("Explicit is better than implicit."), but because flat arguments are
commonly combined with abbreviation/shorthand conventions, which may require
some logic to implement. For example, if only a ``prefix`` is given as a flat
argument, you may want to use the same value to implicitly set the ``suffix``.
To this end, addflat returns the set of keys that it consumed::

        if args:
            used = self.options.addflat(args, ['prefix', 'suffix'])
            if 'suffix' not in used:
                self.options.suffix = self.options.prefix

