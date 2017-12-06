from re import compile

import pytest

from nerodia.exception import UnknownObjectException

pytestmark = pytest.mark.page('images.html')


class TestMapExist(object):
    def test_returns_true_if_the_element_exists(self, browser):
        assert browser.map(id='triangle_map').exists is True
        assert browser.map(id=compile(r'triangle_map')).exists is True
        assert browser.map(name='triangle_map').exists is True
        assert browser.map(name=compile(r'triangle_map')).exists is True
        assert browser.map(index=0).exists is True
        assert browser.map(xpath="//map[@id='triangle_map']").exists is True

    def test_returns_the_first_map_if_given_no_args(self, browser):
        assert browser.map().exists

    def test_returns_false_if_the_element_does_not_exist(self, browser):
        assert browser.map(id='no_such_id').exists is False
        assert browser.map(id=compile(r'no_such_id')).exists is False
        assert browser.map(name='no_such_name').exists is False
        assert browser.map(name=compile(r'no_such_name')).exists is False
        assert browser.map(index=1337).exists is False
        assert browser.map(xpath="//map[@id='no_such_id']").exists is False

    def test_raises_correct_exception_when_what_argument_is_invalid(self, browser):
        with pytest.raises(TypeError):
            browser.map(id=3.14).exists

    def test_raises_correct_exception_when_how_argument_is_invalid(self, browser):
        from nerodia.exception import MissingWayOfFindingObjectException
        with pytest.raises(MissingWayOfFindingObjectException):
            browser.map(no_such_how='some_value').exists


class TestMapAttributes(object):
    # id
    def test_returns_the_id_if_the_element_exists_and_has_id(self, browser):
        assert browser.map(index=0).id == 'triangle_map'

    def test_returns_an_empty_string_if_the_element_exists_and_the_id_doesnt(self, browser):
        assert browser.map(index=1).id == ''

    def test_raises_correct_exception_for_id_if_the_element_doesnt_exist(self, browser):
        with pytest.raises(UnknownObjectException):
            browser.map(index=1337).id

    # name
    def test_returns_the_name_if_the_element_exists_and_has_name(self, browser):
        assert browser.map(index=0).name == 'triangle_map'

    def test_returns_an_empty_string_if_the_element_exists_and_the_name_doesnt(self, browser):
        assert browser.map(index=1).name == ''

    def test_raises_correct_exception_for_name_if_the_element_doesnt_exist(self, browser):
        with pytest.raises(UnknownObjectException):
            browser.map(index=1337).name


def test_finds_all_attribute_methods(browser):
    assert hasattr(browser.map(index=0), 'id')
    assert hasattr(browser.map(index=0), 'name')
