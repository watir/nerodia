import pytest
from re import compile

pytestmark = pytest.mark.page('images.html')

class TestAreaExist(object):
    def test_returns_true_if_the_area_exists(self, browser):
        assert browser.area(id='NCE').exists
        assert browser.area(id=compile(r'NCE')).exists
        assert browser.area(title='Tables').exists
        assert browser.area(title=compile(r'Tables')).exists

        # TODO: xfail IE
        assert browser.area(href='tables.html').exists

        assert browser.area(href=compile(r'tables')).exists

        assert browser.area(index=0).exists
        assert browser.area(xpath="//area[@id='NCE']").exists

    def test_returns_the_first_area_if_given_no_args(self, browser):
        assert browser.area().exists

    def test_returns_false_if_the_area_doesnt_exist(self, browser):
        assert not browser.area(id='no_such_id').exists
        assert not browser.area(id=compile(r'no_such_id')).exists
        assert not browser.area(title='no_such_title').exists
        assert not browser.area(title=compile(r'no_such_title')).exists

        assert not browser.area(href='no-tables.html').exists
        assert not browser.area(href=compile(r'no-tables')).exists

        assert not browser.area(index=1337).exists
        assert not browser.area(xpath="//area[@id='no_such_id']").exists

    def test_raises_correct_exception_when_what_argument_is_invalid(self, browser):
        with pytest.raises(TypeError):
            browser.area(id=3.14).exists

    def test_raises_correct_exception_when_how_argument_is_invalid(self, browser):
        from watir_snake.exception import MissingWayOfFindingObjectException
        with pytest.raises(MissingWayOfFindingObjectException):
            browser.area(no_such_how='some_value').exists


class TestAreaId(object):
    def test_returns_the_id_attribute(self, browser):
        assert browser.area(index=0).id == 'NCE'

    def test_returns_empty_string_if_element_exists_and_attribute_doesnt(self, browser):
        assert browser.area(index=2).id == ''

    @pytest.mark.parametrize('selector',
                             [{'id': 'no_such_id'},
                              {'index': 1337}])
    def test_raises_correct_exception_if_the_area_doesnt_exist(self, browser, selector):
        from watir_snake.exception import UnknownObjectException
        with pytest.raises(UnknownObjectException):
            browser.area(**selector).id


def test_finds_all_attribute_methods(browser):
    assert hasattr(browser.area(index=0), 'id')
