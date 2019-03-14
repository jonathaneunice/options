An Example
==========

Because the capability of ``options`` is designed for high-end, edge-case
situations, it's hard to demonstrate its virtues with simple code. But we'll
give it a shot.

::

    from options import Options, attrs

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
            print(attrs(opts))

    one = Shape(name='one')
    one.draw()
    one.draw(color='red')
    one.draw(color='green', width=22)

yielding::

    color='white', width=10, name='one', height=10
    color='red', width=10, name='one', height=10
    color='green', width=22, name='one', height=10

So far we could do this with instance variables and standard arguments. It
might look a bit like this::

    class ClassicShape(object):

        def __init__(self, name=None, color='white', height=10, width=10):
            self.name   = name
            self.color  = color
            self.height = height
            self.width  = width

but when we got to the ``draw`` method, things would be quite a bit messier.::

        def draw(self, **kwargs):
            name   = kwargs.get('name',   self.name)
            color  = kwargs.get('color',  self.color)
            height = kwargs.get('height', self.height)
            width  = kwargs.get('width',  self.width)
            print("color={0!r}, width={1}, name={2!r}, height={3}".format(color, width, name, height))

One problem here is that we broke apart the values provided to
``__init__()`` into separate instance variables, now we need to
re-assemble them into something unified.  And we need to explicitly
choose between the ``**kwargs`` and the instance variables.  It
gets repetitive, and is not pretty. Another classic alternative,
using native keyword arguments, is no better::

        def draw2(self, name=None, color=None, height=None, width=None):
            name   = name   or self.name
            color  = color  or self.color
            height = height or self.height
            width  = width  or self.width
            print("color={0!r}, width={1}, name={2!r}, height={3}".format(color, width, name, height))

If we add just a few more instance variables, we've arrived at the `Mr.
Creosote <http://en.wikipedia.org/wiki/Mr_Creosote>`_ of class design. For
every instance variable that might be overridden in a method call, that
method needs one line of code to decide whether the override is, in fact, in
effect. And that line will appear in every method call needing to support
such overrides. Suddenly, dealing with parameters starts to be a full-time
job and responsibility of every method. That's neither elegant nor scalable.
Pretty soon we're in "just one more wafer-thin mint..." territory.

But with ``options``, it's easy. No matter how many configuration variables there
are to be managed, each method needs just one line of code to manage them::

    opts = self.options.push(kwargs)

Changing things works simply and logically::

    Shape.options.set(color='blue')
    one.draw()
    one.options.set(color='red')
    one.draw(height=100)
    one.draw(height=44, color='yellow')

yields::

    color='blue', width=10, name='one', height=10
    color='red', width=10, name='one', height=100
    color='yellow', width=10, name='one', height=44

In one line, we reset the default color for all ``Shape`` objects. That's
visible in the next call to ``one.draw()``. Then we set the instance color
of ``one`` (all other ``Shape`` instances remain blue). Finally, we call
one with a temporary override of the color.

A common pattern makes this even easier::

    class Shape(OptionsClass):
        ...

The ``OptionsClass`` base class will provide a ``set()`` method so that you
don't need ``Shape.options.set()``. ``Shape.set()`` does the same thing,
resulting in an even simpler API. The ``set()`` method is a "combomethod"
that will take either a class or an instance and "do the right thing."
``OptionsClass`` also provides a ``settings()`` method to easily handle
transient ``with`` contexts (more on this in a minute), and a ``__repr__()``
method so that it prints nicely.

The more options and settings a class has, the more unwieldy the
class and instance variable approach becomes, and the more desirable
the delegation alternative. Inheritance is a great software pattern
for many situations--but it's poor pattern for complex option and
configuration handling.

For richly-featured APIs, ``options``'s delegation pattern is simpler. As
the number of options grows, delegation imposes almost no additional coding,
complexity, or failure modes. Options are consolidated in one place,
providing neat attribute-style access and keeping everything tidy. We can
add new options or methods with confidence::

    def is_tall(self, **kwargs):
        opts = self.options.push(kwargs)
        return opts.height > 100

Under the covers, ``options`` uses a variation on the ``ChainMap`` data
structure (a multi-layer dictionary) to provide option stacking. Every
option set is stacked on top of previously set option sets, with lower-level
values shining through if they're not set at higher levels. This stacking or
overlay model resembles how local and global variables are managed in many
programming languages.

This makes advanced use cases, such as temporary value changes, easy::

    with one.settings(height=200, color='purple'):
        one.draw()
        if is_tall(one):
            ...         # it is, but only within the ``with`` context

    if is_tall(one):    # nope, not here!
        ...

.. note:: You will still need to do some housekeeping in your class's
    ``__init__()`` method, including creating a new options layer.
    If you don't wish to inherit from ``OptionsClass``, you can
    manually add ``set()`` and ``settings()`` methods to your own class.
    See the ``OptionsClass`` source code for details.

As one final feature, consider "magical" parameters. Add the following
code to your class description::

    options.magic(
        height = lambda v, cur: cur.height + int(v) if isinstance(v, str) else v,
        width  = lambda v, cur: cur.width  + int(v) if isinstance(v, str) else v
    )

Now, in addition to absolute ``height`` and ``width`` parameters specified with
``int`` (integer/numeric) values, your module
auto-magically supports relative parameters for ``height`` and ``width`` given
as string parameters.::

    one.draw(width='+200')

yields::

    color='blue', width=210, name='one', height=10

Neat, huh?

For more backstory, see `this StackOverflow.com discussion of how to combat
"configuration sprawl"
<http://stackoverflow.com/questions/11702437/where-to-keep-options-values-paths-to-important-files-etc/11703813#11703813>`_.
For examples of ``options`` in use, see `say <https://pypi.org/project/say/>`_
and `show <https://pypi.org/project/show>`_.
