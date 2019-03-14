Loading From Configuration Files
================================

``options`` values can be easily writen to, or read from,
configuration files. E.g. reading from JSON and YAML with
a low-level approach::

    import json
    o = Options()
    jdata = json.load(open('config.json'))
    o.update(jdata)

Or for YAML::

    import yaml
    o = Options()
    ydata = yaml.load(open('config.yml').read())
    o.update(ydata)

At a higher level, ``Options`` objects contain a ``write`` method
that will directly write the object to a JSON file, and a ``read``
class method that will construct an ``Options`` object from a JSON file.
