import os

import pytest


@pytest.mark.page('wait.html')
class TestElementPresent(object):
    def test_returns_true_if_the_element_exists_and_is_visible(self, browser):
        assert browser.div(id='foo').present

    def test_returns_false_if_the_element_exists_but_is_not_visible(self, browser):
        assert not browser.div(id='bar').present

    def test_returns_false_if_the_element_does_not_exist(self, browser):
        assert not browser.div(id='should-not-exist').present

    def test_returns_false_if_the_element_is_stale(self, browser):
        element = browser.div(id='foo')
        element.exists

        browser.refresh()

        assert element.stale
        assert not element.present

    def test_returns_true_the_second_time_if_the_element_is_stale(self, browser):
        element = browser.div(id='foo')
        element.exists

        browser.refresh()

        assert element.stale
        assert not element.present
        assert element.present


@pytest.mark.page('forms_with_input_elements.html')
class TestElementEnabled(object):
    def test_returns_true_if_the_element_is_enabled(self, browser):
        assert browser.button(name='new_user_submit').enabled

    def test_returns_false_if_the_element_is_disabled(self, browser):
        assert not browser.button(name='new_user_submit_disabled').enabled

    @pytest.mark.usefixtures('quick_timeout')
    def test_correct_exception_if_the_element_doesnt_exist(self, browser):
        from nerodia.exception import UnknownObjectException
        with pytest.raises(UnknownObjectException):
            browser.button(name='no_such_name').enabled


@pytest.mark.page('forms_with_input_elements.html')
class TestElementStale(object):
    def test_returns_true_if_the_element_is_stale(self, browser):
        element = browser.button(name='new_user_submit_disabled')
        element.exists

        browser.refresh()

        assert element.stale

    def test_returns_false_if_the_element_is_not_stale(self, browser):
        element = browser.button(name='new_user_submit_disabled')
        element.exists

        assert not element.stale


@pytest.mark.page('removed_element.html')
class TestElementExists(object):
    def test_element_from_a_collection_returns_false_when_it_becomes_stale(self, browser):
        element = browser.divs(id='text')[0]
        element.exists

        browser.refresh()

        assert element.stale
        assert not element.present

    def test_returns_false_when_tag_name_does_not_match_id(self, browser):
        assert not browser.span(id='text').exists


@pytest.mark.xfail_ie(reason='currently IE throws NoSuchElementException instead of Stale')
@pytest.mark.page('removed_element.html')
class TestElementCall(object):
    def test_handles_exceptions_when_taking_an_action_on_a_stale_element(self, browser):
        element = browser.div(id='text')
        element.exists

        browser.refresh()

        assert element.stale
        element.text


@pytest.mark.page('hover.html')
class TestElementHover(object):
    # TODO: xfail IE, safari

    @pytest.mark.skipif(os.environ.get('CI') == 'true', reason='Very flaky on Travis only')
    def test_should_hover_over_the_element(self, browser):
        link = browser.link()

        assert link.style('font-size') == '10px'
        link.hover()
        link.wait_until(lambda e: e.style('font-size') == '20px', timeout=30)
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
        rep = repr(elements[-1])
        assert "'tag_name': 'frame'" in rep
        assert "'index': -1" in rep

    @pytest.mark.page('wait.html')
    def test_displays_selector_string_for_nested_element(self, browser):
        element = browser.div(index=1).div(id='div2')
        left, right = repr(element).split('-->')
        assert "'index': 1" in left
        assert "'tag_name': 'div'" in left
        assert "'id': 'div2'" in right
        assert "'tag_name': 'div'" in right

    def test_displays_selector_string_for_nested_element_under_frame(self, browser):
        element = browser.iframe(id='one').iframe(id='three')
        left, right = repr(element).split('-->')
        assert "'tag_name': 'iframe'" in left
        assert "'id': 'one'" in left
        assert "'tag_name': 'iframe'" in right
        assert "'id': 'three'" in right
