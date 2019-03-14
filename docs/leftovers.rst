Leftovers
=========

``options`` expects you to define all feasible and legitimate options at the
class level, and to give them reasonable defaults.

None of the initial settings ever have magic applied. Much of the
expected interpretation "magic" will be relative settings, and relative settings
require a baseline value. The top level is expected and demanded to provide a
reasonable baseline.

Any options set "further down" such as when an instance is created or a method
called should set keys that were already-defined at the class level.

However, there are cases where "extra" ``**kwargs`` values may be
provided and make sense. Your object might be a very high level
entry point, for example, representing very large buckets of
functionality, with many options. Some of those options are relevant
to the current instance, while others are intended as pass-throughs
for lower-level modules/objects. This may seem a doubly rarefied
case--and it is, relatively speaking. But `it does happen
<https://pypi.python.org/pypi/show>`_--and when you need multi-level
processing, it's really, really super amazingly handy to have it.

``options`` supports this in its core ``push()`` method by taking
the values that are known to be part of the class's options, and
deleting those from ``kwargs``. Any values left over in the ``kwargs``
``dict`` are either errors, or intended for other recipients.

As yet, there is no automatic check for leftovers.

