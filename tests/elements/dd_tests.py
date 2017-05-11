import pytest
from re import compile

pytestmark = pytest.mark.page('definition_lists.html')


class TestDdExist(object):
    def test_returns_true_if_the_dd_exists(self, browser):
        assert browser.dd(id='someone').exists
        assert browser.dd(class_name='name').exists
        assert browser.dd(xpath="//dd[@id='someone']").exists
        assert browser.dd(index=0).exists

    def test_returns_the_first_dd_if_given_no_args(self, browser):
        assert browser.dd().exists

    def test_returns_false_if_the_dd_doesnt_exist(self, browser):
        assert not browser.dd(id='no_such_id').exists

    def test_raises_correct_exception_when_what_argument_is_invalid(self, browser):
        with pytest.raises(TypeError):
            browser.dd(id=3.14).exists

    def test_raises_correct_exception_when_how_argument_is_invalid(self, browser):
        from watir_snake.exception import MissingWayOfFindingObjectException
        with pytest.raises(MissingWayOfFindingObjectException):
            browser.dd(no_such_how='some_value').exists


class TestDdAttributes(object):
    # class_name

    def test_returns_the_class_name_if_element_exists(self, browser):
        assert browser.dd(id='someone').class_name == 'name'

    def test_returns_an_empty_string_if_element_exists_but_class_name_doesnt(self, browser):
        assert browser.dd(id='city').class_name == ''

    @pytest.mark.parametrize('selector',
                             [{'id': 'no_such_id'},
                              {'title': 'no_such_title'},
                              {'index': 1337},
                              {'xpath': "//dd[@id='no_such_id']"}])
    def test_raises_correct_exception_for_class_name_if_element_does_not_exist(self, browser, selector):
        from watir_snake.exception import UnknownObjectException
        with pytest.raises(UnknownObjectException):
            browser.dd(**selector).class_name

    # id

    def test_returns_the_id_attribute_if_element_exists(self, browser):
        assert browser.dd(class_name='name').id == 'someone'

    def test_returns_an_empty_string_if_element_exists_but_id_doesnt(self, browser):
        assert browser.dd(class_name='address').id == ''

    @pytest.mark.parametrize('selector',
                             [{'id': 'no_such_id'},
                              {'title': 'no_such_title'},
                              {'index': 1337}])
    def test_raises_correct_exception_for_class_name_if_element_does_not_exist(self, browser, selector):
        from watir_snake.exception import UnknownObjectException
        with pytest.raises(UnknownObjectException):
            browser.dd(**selector).id

    # title

    def test_returns_the_title_of_the_element(self, browser):
        assert browser.dd(class_name='name').title == 'someone'

    # text

    def test_returns_the_text_of_the_element(self, browser):
        assert browser.dd(id='someone').text == 'John Doe'

    def test_returns_an_empty_string_if_element_exists_but_contains_no_text(self, browser):
        assert browser.dd(class_name='noop').text == ''

    @pytest.mark.parametrize('selector',
                             [{'id': 'no_such_id'},
                              {'title': 'no_such_title'},
                              {'index': 1337},
                              {'xpath': "//dd[@id='no_such_id']"}])
    def test_raises_correct_exception_for_class_name_if_element_does_not_exist(self, browser, selector):
        from watir_snake.exception import UnknownObjectException
        with pytest.raises(UnknownObjectException):
            browser.dd(**selector).text


def test_finds_all_attribute_methods(browser):
    assert hasattr(browser.dd(index=0), 'id')
    assert hasattr(browser.dd(index=0), 'class_name')
    assert hasattr(browser.dd(index=0), 'style')
    assert hasattr(browser.dd(index=0), 'text')
    assert hasattr(browser.dd(index=0), 'title')


class TestButtonManipulation(object):
    # click

    def test_fires_events_when_clicked(self, browser):
        dd = browser.dd(title='education')
        assert dd.text != 'changed'
        dd.click()
        assert dd.text == 'changed'

    @pytest.mark.parametrize('selector',
                             [{'id': 'no_such_id'},
                              {'title': 'no_such_title'},
                              {'index': 1337},
                              {'xpath': "//dd[@id='no_such_id']"}])
    def test_raises_correct_exception_if_element_doesnt_exist(self, browser, selector):
        from watir_snake.exception import UnknownObjectException
        with pytest.raises(UnknownObjectException):
            browser.dd(**selector).click()

    # html

    def test_returns_the_html_of_the_element(self, browser):
        html = browser.dd(id='someone').html
        assert compile(r'John Doe').search(html)
        assert '</body>' not in html
