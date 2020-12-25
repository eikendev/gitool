from gitool.util import *


def test_list_properties():
    assert list_properties(["ahead", "behind"]) == "ahead and behind"
