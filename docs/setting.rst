Setting and Unsetting
=====================

Using ``options``, objects often become "entry points" that represent both
a set of capabilities and a set of configurations for how that functionality
will be used. As a result, you may want to be able to set the object's
values directly, without referencing their underlying ``options``. It's
convenient to add a ``set()`` method, then use it, as follows::

    def set(self, **kwargs):
        self.options.set(**kwargs)

    one.set(width='*10', color='orange')
    one.draw()

yields::

    color='orange', width=100, name='one', height=10

``one.set()`` is now the equivalent of ``one.options.set()``. Or continue using
the ``options`` attribute explicitly, if you prefer that.

Values can also be unset.::

    from options import Unset

    one.set(color=Unset)
    one.draw()

yields::

    color='blue', width=100, name='one', height=10

Because ``'blue'`` was the color to which ``Shape`` had be most recently set.
With the color of the instance unset, the color of the class shines through.

.. note:: While options are ideally accessed with an attribute notion,
    the preferred of setting options is through method calls: ``set()`` if
    accessing directly, or ``push()`` if stacking values as part of a method call.
    These perform the interpretation and unsetting magic;
    straight assignment does not. In the future, ``options`` may provide an
    equivalent ``__setattr__()`` method to allow assignment--but not yet.

