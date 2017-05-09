import pytest
from re import compile

from watir_snake.exception import UnknownObjectException


class TestAreaExist(object):
    def test_returns_true_if_the_area_exists(self, browser, page):
        page.load('images.html')
        assert browser.area(id='NCE').exists is True
        assert browser.area(id=compile(r'NCE')).exists is True
        assert browser.area(title='Tables').exists is True
        assert browser.area(title=compile(r'Tables')).exists is True

        # TODO: xfail IE
        assert browser.area(href='tables.html').exists is True

        assert browser.area(href=compile(r'tables')).exists is True

        assert browser.area(index=0).exists is True
        assert browser.area(xpath="//area[@id='NCE']").exists is True

    def test_returns_the_first_area_if_given_no_args(self, browser, page):
        page.load('images.html')
        assert browser.area().exists is True

    def test_returns_false_if_the_area_doesnt_exist(self, browser, page):
        page.load('images.html')
        assert browser.area(id='no_such_id').exists is False
        assert browser.area(id=compile(r'no_such_id')).exists is False
        assert browser.area(title='no_such_title').exists is False
        assert browser.area(title=compile(r'no_such_title')).exists is False

        assert browser.area(href='no-tables.html').exists is False
        assert browser.area(href=compile(r'no-tables')).exists is False

        assert browser.area(index=1337).exists is False
        assert browser.area(xpath="//area[@id='no_such_id']").exists is False

    def test_raises_correct_exception_when_what_argument_is_invalid(self, browser, page):
        with pytest.raises(TypeError):
            browser.area(id=3.14).exists

    def test_raises_correct_exception_when_how_argument_is_invalid(self, browser, page):
        from watir_snake.exception import MissingWayOfFindingObjectException
        with pytest.raises(MissingWayOfFindingObjectException):
            browser.area(no_such_how='some_value').exists


class TestAreaId(object):
    def test_returns_the_id_attribute(self, browser, page):
        page.load('images.html')
        assert browser.area(index=0).id == 'NCE'

    def test_returns_empty_string_if_element_exists_and_attribute_doesnt(self, browser, page):
        page.load('images.html')
        assert browser.area(index=2).id == ''

    @pytest.mark.parametrize('selector',
                             [{'id': 'no_such_id'},
                              {'index': 1337}])
    def test_raises_correct_exception_if_the_area_doesnt_exist(self, browser, page, selector):
        with pytest.raises(UnknownObjectException):
            browser.area(**selector).id


def test_finds_all_attribute_methods(browser, page):
    page.load('images.html')
    assert hasattr(browser.area(index=0), 'id')
