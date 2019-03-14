options
=======

``options`` sotres option and configuration data in a clean, high-function way.
Changes can "overlay" defaults or earlier settings.

For most code, ``options`` is flexibility overkill. Not everyone wants to be a
world-class gymnast, yogi, or contortionist. For most functions and classes,
Python's regular arguments, ``*args``, ``**kwargs``, and inheritance patterns
are elegant and sufficient. ``options`` is for the top 1% that need:

  * extremely functional classes, functions, and methods,
  * with many different features and options,
  * the settings for which might be adjusted or overriden at any time,
  * yet that need "reasonable" or "intelligent" defaults, and
  * that yearn for a simple, unobtrusive API.

In those cases, Python's built-in, inheritance-based model stops being the
simple approach. Non-trivial argument-management code and complexity
begins to pervade. This is where ``options``'s layered, delegation-based
approach begins to shine. Almost regardless of how varied the options it
wrangles, or how much flexibility is required, code complexity remains flat.

.. figure:: http://content.screencast.com/users/jonathaneunice/folders/Jing/media/02e27ff4-402d-4450-b3ee-2c7be26eb05b/00000014.png
   :align: center

Python has very flexible arguments for functions and methods, and
good connection of values from classes to subclasses to methods.
It doesn't, however, connect those very well to configuration files,
module defaults, method parameters, and other uses. ``options``,
in contrast, seamlessly connects all of these varied layers and cases.

For more backstory, see `this StackOverflow.com discussion of how to combat "configuration sprawl"
<http://stackoverflow.com/questions/11702437/where-to-keep-options-values-paths-to-important-files-etc/11703813#11703813>`_.
For examples of ``options``
in use, see `say <https://pypi.org/project/say>`_, `quoter <https://pypi.org/project/quoter>`_,
and `show <https://pypi.org/project/show>`_.


.. toctree::
   :titlesonly:

   Usage <usage>
   An Example <example>
   Design Considerations <design>
   Setting and Unsetting <setting>
   Leftovers <leftovers>
   Magic Parameters <magic>
   The Magic APIs <magicapis>
   Subclassing <subclassing>
   Transients and Internal Options <transients>
   Flat Arguments <flatargs>
   Choosing Option Names <names>
   Special Values <specialvals>
   Loading From Configuration Files <config>
   Related Work <related>
   Notes <notes>
   Installation <installation>
   CHANGES
