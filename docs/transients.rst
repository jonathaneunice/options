Transients and Internal Options
===============================

Some options do not make sense as permanent values--they are needed only as
transient settings in the context of individual method calls. The special null value
``Transient`` can be assigned as an option value to signal this.

Other options are useful, but only internal to your class. They are not meant to
be exposed as part of the external API. In this case, they can be signified
by prefixing with an underscore, such as ``_cached_value``. This is consistent
with Python naming practice.
