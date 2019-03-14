Usage
=====

In a typical use of ``options``, your highly-functional class defines
default values. Subclasses can add, remove, or override options.
Instances use class defaults, but they can be overridden when each instance
is created. For any option an instance doesn't override, the class default
"shines through."

So far, this isn't very different from a typical use of Python's standard
instance and class variables. The next step is where ``options`` gets
interesting.

Individual method calls can similarly override instance and class defaults.
The options stated in each method call obtain only for the duration of the
method's execution. If the call doesn't set a value, the instance value
applies. If the instance didn't set a value, the class default applies (and
so on, to its superclasses, if any).

One step further, Python's ``with`` statement can be used to
set option values for just a specific duration. As soon as the
``with`` block exists, the option values automagically fall back to
what they were before the block. (In general, if any option is unset,
its value falls back to what it was in the next higher layer.)

To recap: Python handles class, subclass, and instance settings. ``options``
handles these as well, but also adds method and transient settings. By
default when Python overrides a setting, it's destructive; the value cannot
be "unset" without additional code. When a program using ``options``
overrides a setting, it does so non-destructively, layering the new settings
atop the previous ones. When attributes are unset, they immediately fall
back to their prior value (at whatever higher level it was last set).

