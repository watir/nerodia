import pytest


@pytest.mark.page('wait.html')
class TestElementPresent(object):
    def test_returns_true_if_the_element_exists_and_is_visible(self, browser):
        assert browser.div(id='foo').present

    def test_returns_false_if_the_element_exists_but_is_not_visible(self, browser):
        assert not browser.div(id='bar').present

    def test_returns_false_if_the_element_does_not_exist(self, browser):
        assert not browser.div(id='should-not-exist').present

    def test_returns_false_if_the_element_is_stale(self, browser, mocker):
        wd_element = browser.div(id='foo').wd

        # simulate element going stale during lookup
        mock = mocker.patch('selenium.webdriver.remote.webdriver.WebDriver.find_element')
        mock.return_value = wd_element
        browser.refresh()

        assert not browser.div(id='foo').present


@pytest.mark.page('forms_with_input_elements.html')
class TestElementEnabled(object):
    def test_returns_true_if_the_element_is_enabled(self, browser):
        assert browser.element(name='new_user_submit').enabled

    def test_returns_false_if_the_element_is_disabled(self, browser):
        assert not browser.element(name='new_user_submit_disabled').enabled

    def test_correct_exception_if_the_element_doesnt_exist(self, browser):
        from watir_snake.exception import UnknownObjectException
        with pytest.raises(UnknownObjectException):
            browser.element(name='no_such_name').enabled


@pytest.mark.page('removed_element.html')
class TestElementExists(object):
    def test_relocates_element_from_a_collection_when_it_becomes_stale(self, browser):
        element = browser.divs(id='text')[0]
        assert element.exists
        browser.refresh()
        assert element.exists

    def test_returns_false_when_tag_name_does_not_match_id(self, browser):
        assert not browser.span(id='text').exists


@pytest.mark.page('removed_element.html')
class TestElementCall(object):
    def test_handles_exceptions_when_taking_an_action_on_an_element_that_goes_stale_during_execution(self, browser, mocker):
        made = []

        def make_stale():
            if not made:
                browser.refresh()
                made.append(True)

        element = browser.div(id='text')
        mock = mocker.patch('watir_snake.elements.element.Element.assert_element_found')
        mock.side_effect = make_stale
        element.text


@pytest.mark.page('hover.html')
class TestElementHover(object):
    # TODO: xfail Firefox, IE, safari
    def test_should_hover_over_the_element(self, browser):
        link = browser.link()

        assert link.style('font-size') == '10px'
        link.hover()
        assert link.style('font-size') == '20px'


@pytest.mark.page('nested_iframes.html')
class TestElementRepr(object):
    def test_displays_specified_element_type(self, browser):
        assert 'Div' in repr(browser.div())

    def test_does_not_display_specified_element_type_if_not_specified(self, browser):
        assert 'HTMLElement' in repr(browser.element(index=4))

    def test_displays_keyword_if_specified(self, browser):
        element = browser.h3()
        element.keyword = 'foo'
        assert 'keyword: foo' in repr(element)

    def test_does_not_display_keyword_if_not_specified(self, browser):
        assert 'keyword: foo' not in repr(browser.h3())

    def test_locate_is_false_when_not_located(self, browser):
        assert 'located: False' in repr(browser.div(id='not_present'))

    def test_locate_is_true_when_located(self, browser):
        element = browser.h3()
        element.exists
        assert 'located: True' in repr(element)

    def test_displays_selector_string_for_element_from_collection(self, browser):
        elements = browser.frames()
        assert "'index': -1, 'tag_name': 'frame'" in repr(elements[-1])

    @pytest.mark.page('wait.html')
    def test_displays_selector_string_for_nested_element(self, browser):
        element = browser.div(index=1).div(id='div2')
        assert "{'index': 1, 'tag_name': 'div'} --> {'tag_name': 'div', 'id': 'div2'" in repr(element)

    def test_displays_selector_string_for_nested_element_under_frame(self, browser):
        element = browser.iframe(id='one').iframe(id='three')
        assert "{'tag_name': 'iframe', 'id': 'one'} --> {'tag_name': 'iframe', 'id': 'three'" in repr(element)
