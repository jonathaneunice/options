Magic Parameters
================

Python's ``*args`` variable-number of arguments and ``**kwargs`` keyword
arguments are sometimes called "magic" arguments. ``options`` takes this up a
notch, allowing setters much like Python's ``property`` function or
``@property`` decorator. This allows arguments to be interpreted on the fly.
This is useful, for instance, to provide relative rather than just absolute
values. As an example, say that we added this code after ``Shape.options`` was
defined::

    options.magic(
        height = lambda v, cur: cur.height + int(v) if isinstance(v, str) else v,
        width  = lambda v, cur: cur.width  + int(v) if isinstance(v, str) else v
    )

Now, in addition to absolute ``height`` and ``width`` parameters which are
provided by specifying ``int`` (integer/numeric) values, your module
auto-magically supports relative parameters for ``height`` and ``width``.::

    one.draw(width='+200')

yields::

    color='blue', width=210, name='one', height=10

This can be as fancy as you like, defining an entire domain-specific expression language.
But even small functions can give you a great bump in expressive power. For example,
add this and you get full relative arithmetic capability (``+``, ``-``, ``*``, and ``/``)::

    def relmath(value, currently):
        if isinstance(value, str):
            if value.startswith('*'):
                return currently * int(value[1:])
            elif value.startswith('/'):
                return currently / int(value[1:])
            else:
                return currently + int(value)
        else:
            return value

    ...

    options.magic(
        height = lambda v, cur: relmath(v, cur.height),
        width  = lambda v, cur: relmath(v, cur.width)
    )

Then::

    one.draw(width='*4', height='/2')

yields::

    color='blue', width=40, name='one', height=5

Magically interpreted parameters are the sort of thing that one doesn't need
very often or for every parameter--but when they're useful, they're *enormously*
useful and highly leveraged, leading to much simpler, much higher function APIs.

We call them 'magical' here because of the "auto-magical" interpretation, but
they are really just analogs of Python object properties. The magic function is
basically a "setter" for a dictionary element.

