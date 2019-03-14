from options.config import *
import pytest


def test_read_write(tmpdir):
    tname1 = str(tmpdir.join("test1.json"))
    tname2 = str(tmpdir.join("test2.json"))

    d = dict(color='red', shape='box', count=44, value=12.1)
    write_dict(d, tname1)
    rd = read_dict(tname1)
    assert d == rd
