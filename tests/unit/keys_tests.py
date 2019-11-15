from nerodia.keys import Keys


def test_can_access_keys():
        assert Keys.TAB == u'\ue004'
    

def test_keys_exists():
    assert isinstance(Keys, object)
