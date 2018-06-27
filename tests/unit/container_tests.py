import pytest

from nerodia.container import Container


class TestContainerExtractSelector(object):
    def test_converts_2_arg_selector_into_a_dict(self):
        assert Container()._extract_selector('how', 'what') == {'how': 'what'}

    def test_returns_the_kwargs_given(self):
        assert Container()._extract_selector(how='what') == {'how': 'what'}

    def test_returns_an_empty_dict_if_given_no_args(self):
        assert Container()._extract_selector() == {}

    def test_raises_correct_exception_if_given_1_arg(self):
        with pytest.raises(ValueError):
            Container()._extract_selector('how')

    def test_raises_correct_exception_if_given_over_2_args(self):
        with pytest.raises(ValueError):
            Container()._extract_selector('how', 'what', 'value')
