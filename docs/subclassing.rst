Subclassing
===========

Subclass options may differ from superclass options. Usually they will share
many options, but some may be added, and others removed. To modify the set of
available options, the subclass defines its options with the ``add()`` method to
the superclass options. This creates a layered
effect, just like ``push()`` for an instance. The difference is, ``push()`` does
not allow new options (keys) to be defined; ``add()`` does. It is also possible to
assign the special null object ``Prohibited``, which will disallow instances of the
subclass from setting those values.::

    options = Superclass.options.add(
        func   = None,
        prefix = Prohibited,  # was available in superclass, but not here
        suffix = Prohibited,  # ditto
    )

Because some of the "additions" can be prohibitions (i.e. removing
particular options from being set or used), this is "adding to" the superclass's
options in the sense of "adding a layer onto" rather than strict "adding
options."

An alternative is to copy (or restate) the superclass's options. That suits
"unlinked" cases--where the subclass is highly independent, and where changes to
the superclass's options should not effect the subclass's options. With
``add()``, they remain linked in the same way as instances and classes are.

