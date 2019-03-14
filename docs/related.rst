Related Work
============

A huge amount of work, both in Python and beyond, has gone into
the effective management of configuration information.

* Program defaults. Values pre-established by developers, often
  as ``ALL_UPPERCASE_IDENTIFIERS`` or as keyword default to
  functions.

* Configuration file format parsers/formatters. Huge amounts of the INI,
  JSON, XML, and YAML specifications and toolchains, for example, are
  configuration-related. There are many. `anyconfig
  <https://pypi.org/project/anyconfig>`_ is perhaps of interest for its
  flexibility. You could probably lump into this group binary data
  marshaling schemes such as ``pickle``.

* Command-line argument parsers. These are all about taking configuration
  information from the command line. `argh
  <https://pypi.org/project/argh>`_ is one I particularly like for its
  simple, declarative nature. (`aaargh
  <https://pypi.org/project/aaargh>`_ is similar.)

* System and environment introspection. The best known of these would be
  ``sys.argv`` and ``os.environ`` to get command line arguments and the
  values of operating system environment variables (especially when running
  on Unixy platforms). But any code that asks "Where am I running?" or
  "What is my IP address?" or otherwise inspects its current execution
  environment and configures itself accordingly is doing a form of
  configuration discovery.

* Attribute-accessible dictionary objects. It is incredibly easy to create
  simple versions of this idea in Python--and rather tricky to create
  robust, full-featured versions. Caveat emptor. `stuf
  <https://pypi.org/project/stuf>`_ and `treedict
  <https://pypi.org/project/treedict>`_ are cream-of-the-crop
  implementations of this idea. I have not tried `confetti
  <https://pypi.org/project/confetti>`_ or `Yaco
  <https://pypi.org/project/Yaco>`_, but they look like interesting
  variations on the same theme.

* The portion of Web frameworks concerned with getting and setting cookies,
  URL query and hash attributes, form variables, and/or HTML5 local
  storage. Not that these are particularly secure, scalable, or robust
  sources...but they're important configuration information nonetheless.

* While slightly afield, database interface modules are often used for
  querying configuration information from SQL or NoSQL databases.

* Some object metaprogramming systems. That's a mouthful, right? Well some
  modules implement metaclasses that change the basic behavior of objects.
  `value <https://pypi.org/project/value>`_ for example provides very
  common-sense treatment of object instantiation with out all the Javaesque
  ``self.x = x; self.y = y; self.z = z`` repetition. ``options`` similarly
  redesigns how parameters should be passed and object values stored.

* Combomatics. Many configuration-related modules combine two or more of
  these approaches. E.g. `yconf <https://pypi.org/project/yconf>`_
  combines YAML config file parsing with ``argparse`` command line parsing.
  In the future, ``options`` will also follow this path. There's no need to
  take programmer time and attention for several different low-level
  configuration-related tasks.

* Dependency injection frameworks are all about providing configuration
  information from outside code modules. They tend to be rather
  abstract and have a high "activation energy," but the more complex
  and composed-of-many-different-components your system is, the
  more valuable the "DI pattern" becomes.

* Other things. `conflib <https://pypi.org/project/conflib>`_, uses
  dictionary updates to stack default, global, and local settings; it also
  provides a measure of validation.

This diversity, while occasionally frustrating, makes some sense.
Configuration data, after all, is just "state," and "managing state" is
pretty much what all computing is about. Pretty much every program has to do
it. That so many use so many different, home-grown ways is why there's such
a good opportunity.

`Flask's documentation
<http://flask.pocoo.org/docs/config/#configuring-from-files>`_ is a
real-world example of how "spread everywhere" this can be, with some data
coming from the program, some from files, some from environment variables,
some from Web-JSON, etc.

