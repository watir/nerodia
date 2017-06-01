import pytest
from re import compile

pytestmark = pytest.mark.page('non_control_elements.html')


class TestDivExist(object):
    def test_returns_true_if_the_element_exists(self, browser):
        assert browser.div(id='header').exists
        assert browser.div(id=compile(r'header')).exists
        assert browser.div(title='Header and primary navigation').exists
        assert browser.div(title=compile(r'Header and primary navigation')).exists
        assert browser.div(text='This is a footer.').exists
        assert browser.div(text=compile(r'This is a footer\.')).exists
        assert browser.div(class_name='profile').exists
        assert browser.div(class_name=compile(r'profile')).exists
        assert browser.div(index=0).exists
        assert browser.div(xpath="//div[@id='header']").exists

    def test_returns_the_first_div_if_given_no_args(self, browser):
        assert browser.div().exists

    def test_returns_false_if_the_element_doesnt_exist(self, browser):
        assert not browser.div(id='no_such_id').exists
        assert not browser.div(id=compile(r'no_such_id')).exists
        assert not browser.div(title='no_such_title').exists
        assert not browser.div(title=compile(r'no_such_title')).exists
        assert not browser.div(text='no_such_text').exists
        assert not browser.div(text=compile(r'no_such_text')).exists
        assert not browser.div(class_name='no_such_class').exists
        assert not browser.div(class_name=compile(r'no_such_class')).exists
        assert not browser.div(index=1337).exists
        assert not browser.div(xpath="//div[@id='no_such_id']").exists

    def test_raises_correct_exception_when_what_argument_is_invalid(self, browser):
        with pytest.raises(TypeError):
            browser.div(id=3.14).exists

    def test_raises_correct_exception_when_how_argument_is_invalid(self, browser):
        from watir_snake.exception import MissingWayOfFindingObjectException
        with pytest.raises(MissingWayOfFindingObjectException):
            browser.div(no_such_how='some_value').exists


class TestDivAttributes(object):
    # class_name

    def test_returns_the_class_name_if_element_exists(self, browser):
        assert browser.div(id='footer').class_name == 'profile'

    def test_returns_an_empty_string_if_element_exists_but_class_name_doesnt(self, browser):
        assert browser.div(id='content').class_name == ''

    @pytest.mark.parametrize('selector',
                             [{'id': 'no_such_id'},
                              {'title': 'no_such_title'},
                              {'index': 1337},
                              {'xpath': "//div[@id='no_such_id']"}])
    def test_raises_correct_exception_for_class_name_if_element_does_not_exist(self, browser, selector):
        from watir_snake.exception import UnknownObjectException
        with pytest.raises(UnknownObjectException):
            browser.div(**selector).class_name

    # id

    def test_returns_the_id_attribute_if_element_exists(self, browser):
        assert browser.div(index=1).id == 'outer_container'

    def test_returns_an_empty_string_if_element_exists_but_id_doesnt(self, browser):
        assert browser.div(index=0).id == ''

    @pytest.mark.parametrize('selector',
                             [{'id': 'no_such_id'},
                              {'title': 'no_such_title'},
                              {'index': 1337}])
    def test_raises_correct_exception_for_id_if_element_does_not_exist(self, browser, selector):
        from watir_snake.exception import UnknownObjectException
        with pytest.raises(UnknownObjectException):
            browser.div(**selector).id

    @pytest.mark.page('multiple_ids.html')
    def test_should_take_all_conditions_into_account_when_locating_by_id(self, browser):
        assert browser.div(id='multiple', class_name='bar').class_name == 'bar'

    # style

    # TODO: xfail IE
    def test_returns_the_style_of_the_element(self, browser):
        assert browser.div(id='best_language').style() == 'color: red; text-decoration: ' \
                                                          'underline; cursor: pointer;'

    def test_returns_an_empty_string_if_element_exists_but_style_doesnt(self, browser):
        assert browser.div(id='promo').style() == ''

    def test_raises_correct_exception_for_title_if_element_does_not_exist(self, browser):
        from watir_snake.exception import UnknownObjectException
        with pytest.raises(UnknownObjectException):
            browser.div(id='no_such_id').style()

    # text

    def test_returns_the_text_of_the_element(self, browser):
        assert browser.div(id='footer').text == 'This is a footer.'
        assert browser.div(title='Closing remarks').text == 'This is a footer.'
        assert browser.div(xpath="//div[@id='footer']").text == 'This is a footer.'

    def test_returns_an_empty_string_if_element_exists_but_contains_no_text(self, browser):
        assert browser.div(index=0).text == ''

    def test_returns_an_empty_string_if_element_is_hidden(self, browser):
        assert browser.div(id='hidden').text == ''

    @pytest.mark.parametrize('selector',
                             [{'id': 'no_such_id'},
                              {'title': 'no_such_title'},
                              {'index': 1337},
                              {'xpath': "//div[@id='no_such_id']"}])
    def test_raises_correct_exception_for_text_if_element_does_not_exist(self, browser, selector):
        from watir_snake.exception import UnknownObjectException
        with pytest.raises(UnknownObjectException):
            browser.delete(**selector).text


def test_finds_all_attribute_methods(browser):
    assert hasattr(browser.div(index=0), 'class_name')
    assert hasattr(browser.div(index=0), 'id')
    assert hasattr(browser.div(index=0), 'style')
    assert hasattr(browser.div(index=0), 'text')


class TestDivManipulation(object):
    # click

    def test_fires_events_when_clicked(self, browser):
        assert not browser.div(id='best_language').text == 'Ruby!'
        browser.div(id='best_language').click()
        assert browser.div(id='best_language').text == 'Ruby!'

    @pytest.mark.parametrize('selector',
                             [{'id': 'no_such_id'},
                              {'title': 'no_such_title'},
                              {'index': 1337},
                              {'xpath': "//div[@id='no_such_id']"}])
    def test_raises_correct_exception_when_clicking_a_div_that_doesnt_exist(self, browser, selector):
        from watir_snake.exception import UnknownObjectException
        with pytest.raises(UnknownObjectException):
            browser.button(**selector).click()

    # TODO: xfail safari
    def test_double_click_fires_the_ondblclick_event(self, browser, messages):
        browser.div(id='html_test').double_click()
        assert 'double clicked' in messages.list

    # TODO: xfail firefox, phantomjs (https://github.com/detro/ghostdriver/issues/125)
    @pytest.mark.page('right_click.html')
    def test_fires_the_oncontextmenu_event(self, browser, messages):
        browser.div(id='click').right_click()
        assert messages.list[0] == 'right-clicked'

    # html

    # TODO xfail IE
    def test_returns_the_html_of_the_element(self, browser):
        html = browser.div(id='footer').html.lower()
        assert 'id="footer"' in html
        assert 'title="closing remarks"' in html
        assert 'class="profile"' in html

        assert '<div id="content">' not in html
        assert '</body>' not in html
