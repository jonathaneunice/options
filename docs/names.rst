Choosing Option Names
=====================

You can choose pretty much any option name that is a legitimate
Python keyword argument. The exceptions: Names that are already
defined by methods of ``Options`` or ``OptionsChain``. To wit:
``add``, ``addflat``, ``clear``, ``copy``, ``fromkeys``, ``get``,
``items``, ``iteritems``, ``iterkeys``, ``itervalues``, ``keys``,
``magic``, ``magical``, ``new_child``, ``parents``, ``pop``,
``popitem``, ``push``, ``read``, ``set``, ``setdefault``, ``update``,
``values``, and ``write`` are off-limits.

If you try to define options with verboten names, a ``BadOptionName``
exception will be raised. This will save you grief down the road;
getting back a wrong thing at runtime is vastly harder to debug
than fielding an early exception.

