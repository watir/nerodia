import pytest


from nerodia.keys import Keys


def test_can_access_keys():
    assert Keys.TAB == '\ue004'


def test_keys_exists():
    assert isinstance(Keys, object)
