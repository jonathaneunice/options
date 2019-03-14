Special Values
==============

Some special values (`"sentinels"
values <http://en.wikipedia.org/wiki/Sentinel_value>`_) are defined:

``Prohibited``
  This option cannot be used (set or accessed). Useful primarily in
  subclasses, to "turn off" options that apply in the superclass, but
  not the subclass.

``Transient``
  Option is not set initially or on a per-instance basis, but may be
  invoked on a call-by-call basis.

``Reserved``
  Not used, but explicitly marked as reserved for future use.

``Unset``
  If an option is set to ``Unset``, the current value
  is removed, letting values from higher up the option chain shine through.

