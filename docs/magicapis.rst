The Magic APIs
==============

The callables (usually functions, lambda expressions, static methods, or methods) called
to preform magical interpretation can be called with 1, 2, or 3 parameters.
``options`` inquires as to how many parameters the callable accepts. If it
accepts only 1, it will be the value passed in. Cleanups like "convert to upper case"
can be done, but no relative interpretation. If it accepts 2 arguments,
it will be called with the value and the current option mapping, in that order.
(NB this order reverses the way you may think logical. Caution advised.) If the
callable requires 3 parameters, it will be ``None``, value, current mapping. This
supports method calls, though has the defect of not really
passing in the current instance.

A decorator form, ``magical()`` is also supported. It must be given the
name of the key exactly::

    @options.magical('name')
    def capitalize_name(self, v, cur):
        return ' '.join(w.capitalize() for w in v.split())

The net is that you can provide just about any kind of callable.
But the meta-programming of the magic interpretation API could use a little work.

