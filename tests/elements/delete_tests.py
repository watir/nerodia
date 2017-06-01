import pytest
from re import compile

pytestmark = pytest.mark.page('non_control_elements.html')


class TestDeleteExist(object):
    def test_returns_true_if_the_delete_exists(self, browser):
        assert browser.delete(id='lead').exists
        assert browser.delete(id=compile(r'lead')).exists
        assert browser.delete(text='This is a deleted text tag 1').exists
        assert browser.delete(text=compile(r'This is a deleted text tag 1')).exists
        assert browser.delete(class_name='lead').exists
        assert browser.delete(class_name=compile(r'lead')).exists
        assert browser.delete(index=0).exists
        assert browser.delete(xpath="//del[@id='lead']").exists

    def test_returns_the_first_delete_if_given_no_args(self, browser):
        assert browser.delete().exists

    def test_returns_false_if_the_delete_doesnt_exist(self, browser):
        assert not browser.delete(id='no_such_id').exists
        assert not browser.delete(id=compile(r'no_such_id')).exists
        assert not browser.delete(text='no_such_text').exists
        assert not browser.delete(text=compile(r'no_such_text')).exists
        assert not browser.delete(class_name='no_such_class').exists
        assert not browser.delete(class_name=compile(r'no_such_class')).exists
        assert not browser.delete(index=1337).exists
        assert not browser.delete(xpath="//del[@id='no_such_id']").exists

    def test_raises_correct_exception_when_what_argument_is_invalid(self, browser):
        with pytest.raises(TypeError):
            browser.delete(id=3.14).exists

    def test_raises_correct_exception_when_how_argument_is_invalid(self, browser):
        from watir_snake.exception import MissingWayOfFindingObjectException
        with pytest.raises(MissingWayOfFindingObjectException):
            browser.delete(no_such_how='some_value').exists


class TestDeleteAttributes(object):
    # class_name

    def test_returns_the_class_name_if_element_exists(self, browser):
        assert browser.delete(index=0).class_name == 'lead'

    def test_returns_an_empty_string_if_element_exists_but_class_name_doesnt(self, browser):
        assert browser.delete(index=2).class_name == ''

    def test_raises_correct_exception_for_class_name_if_element_does_not_exist(self, browser):
        from watir_snake.exception import UnknownObjectException
        with pytest.raises(UnknownObjectException):
            browser.delete(id='no_such_id').class_name

    # id

    def test_returns_the_id_attribute_if_element_exists(self, browser):
        assert browser.delete(index=0).id == 'lead'

    def test_returns_an_empty_string_if_element_exists_but_id_doesnt(self, browser):
        assert browser.delete(index=2).id == ''

    @pytest.mark.parametrize('selector',
                             [{'id': 'no_such_id'},
                              {'index': 1337}])
    def test_raises_correct_exception_for_id_if_element_does_not_exist(self, browser, selector):
        from watir_snake.exception import UnknownObjectException
        with pytest.raises(UnknownObjectException):
            browser.delete(**selector).id

    # title

    def test_returns_the_title_of_the_element(self, browser):
        assert browser.delete(index=0).title == 'Lorem ipsum'

    def test_returns_an_empty_string_if_element_exists_but_title_doesnt(self, browser):
        assert browser.delete(index=2).title == ''

    @pytest.mark.parametrize('selector',
                             [{'id': 'no_such_id'},
                              {'xpath': "//del[@id='no_such_id']"}])
    def test_raises_correct_exception_for_title_if_element_does_not_exist(self, browser, selector):
        from watir_snake.exception import UnknownObjectException
        with pytest.raises(UnknownObjectException):
            browser.delete(**selector).title

    # text

    def test_returns_the_text_of_the_element(self, browser):
        assert browser.delete(index=1).text == 'This is a deleted text tag 2'

    def test_returns_an_empty_string_if_element_exists_but_contains_no_text(self, browser):
        assert browser.delete(index=3).text == ''

    @pytest.mark.parametrize('selector',
                             [{'id': 'no_such_id'},
                              {'xpath': "//del[@id='no_such_id']"}])
    def test_raises_correct_exception_for_text_if_element_does_not_exist(self, browser, selector):
        from watir_snake.exception import UnknownObjectException
        with pytest.raises(UnknownObjectException):
            browser.delete(**selector).text


def test_finds_all_attribute_methods(browser):
    assert hasattr(browser.delete(index=0), 'class_name')
    assert hasattr(browser.delete(index=0), 'id')
    assert hasattr(browser.delete(index=0), 'title')
    assert hasattr(browser.delete(index=0), 'text')


class TestDeleteManipulation(object):
    # click

    def test_fires_events(self, browser):
        delete = browser.delete(class_name='footer')
        assert 'Javascript' not in delete.text
        delete.click()
        assert 'Javascript' in delete.text

    @pytest.mark.parametrize('selector',
                             [{'id': 'no_such_id'},
                              {'title': 'no_such_title'}])
    def test_raises_correct_exception_if_element_doesnt_exist(self, browser, selector):
        from watir_snake.exception import UnknownObjectException
        with pytest.raises(UnknownObjectException):
            browser.delete(**selector).click()
