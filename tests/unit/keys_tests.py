import six


from nerodia.keys import Keys


def test_can_access_keys():
    if six.PY3:
        assert Keys.TAB == '\ue004'
    else:
        assert Keys.TAB == '\\\ue004'


def test_keys_exists():
    assert isinstance(Keys, object)
