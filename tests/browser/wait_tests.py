import re
from time import time

import pytest

import nerodia
from nerodia.exception import ObjectDisabledException, UnknownObjectException, \
    ObjectReadOnlyException
from nerodia.wait.wait import TimeoutError, Wait


@pytest.fixture
def default_timeout_handling():
    orig_timeout = nerodia.default_timeout
    nerodia.default_timeout = 1
    yield
    nerodia.default_timeout = orig_timeout


@pytest.fixture
def refresh_before(browser):
    browser.refresh()
    yield


def executed_within(method, min=0, max=None):
    max = max or min + 1
    nerodia.default_timeout = max
    start = time()
    fail = False
    try:
        method()
    except TimeoutError:
        fail = True
    diff = time() - start
    result = False if fail else max > diff > min
    return result, diff


@pytest.mark.page('wait.html')
@pytest.mark.usefixtures('default_timeout_handling')
class TestDefaultTimeout(object):
    def test_when_no_timeout_is_specified(self, browser):
        start_time = time()
        with pytest.raises(TimeoutError):
            Wait.until(lambda: False)
        assert nerodia.default_timeout < time() - start_time < nerodia.default_timeout + 1

    def test_is_used_by_wait_until_not(self, browser):
        start_time = time()
        with pytest.raises(TimeoutError):
            Wait.until_not(lambda: True)
        assert nerodia.default_timeout < time() - start_time < nerodia.default_timeout + 1

    @pytest.mark.usefixtures('default_timeout_handling')
    def test_ensures_all_checks_happen_once_even_if_time_has_expired(self, browser):
        nerodia.default_timeout = -1
        browser.link.click()  # Fails if exception is raised


@pytest.mark.page('wait.html')
class TestElementWaitUntil(object):
    def test_returns_element_for_additional_actions(self, browser):
        element = browser.div(id='foo')
        assert element.wait_until(lambda e: e.exists) == element

    def test_accepts_self_by_default_in_wait_method(self, browser):
        element = browser.div(id='bar')
        browser.link(id='show_bar').click()
        element.wait_until(lambda el: el.text == 'bar')

    def test_accepts_any_value_in_wait_method(self, browser):
        element = browser.div(id='bar')
        assert element.wait_until(lambda x: x == 'bar', object='bar')

    def test_accepts_just_a_timeout_parameter_with_method(self, browser):
        element = browser.div(id='bar')
        element.wait_until(timeout=0, method=lambda _: True)

    def test_accepts_just_a_message_parameter_with_method(self, browser):
        element = browser.div(id='bar')
        element.wait_until(message='no', method=lambda _: True)

    def test_accepts_just_an_interval_parameter_with_method(self, browser):
        element = browser.div(id='bar')
        element.wait_until(interval=0.1, method=lambda _: True)

    # Keyword

    @pytest.mark.usefixtures('refresh_before')
    def test_accepts_text_keyword(self, browser):
        element = browser.div(id='bar')
        browser.link(id='show_bar').click()
        element.wait_until(text='bar')

    @pytest.mark.usefixtures('refresh_before')
    def test_accepts_regexp_value(self, browser):
        element = browser.div(id='bar')
        browser.link(id='show_bar').click()
        element.wait_until(style=re.compile(r'block'))

    @pytest.mark.usefixtures('refresh_before')
    def test_accepts_multiple_keywords(self, browser):
        element = browser.div(id='bar')
        browser.link(id='show_bar').click()
        element.wait_until(text='bar', style=re.compile(r'block'))

    @pytest.mark.usefixtures('refresh_before')
    def test_accepts_custom_keyword(self, browser):
        element = browser.div(id='bar')
        browser.link(id='show_bar').click()
        element.wait_until(custom='bar')

    @pytest.mark.usefixtures('refresh_before', 'default_timeout_handling')
    def test_times_out_when_single_keyword_not_met(self, browser):
        element = browser.div(id='bar')
        with pytest.raises(TimeoutError):
            element.wait_until(id='foo')

    @pytest.mark.usefixtures('refresh_before', 'default_timeout_handling')
    def test_times_out_when_one_of_multiple_keywords_not_met(self, browser):
        element = browser.div(id='bar')
        with pytest.raises(TimeoutError):
            element.wait_until(id='foo', text='foo')

    @pytest.mark.usefixtures('refresh_before', 'default_timeout_handling')
    def test_times_out_when_a_custom_keyword_not_met(self, browser):
        element = browser.div(id='bar')
        with pytest.raises(TimeoutError):
            element.wait_until(custom='foo')


@pytest.mark.page('wait.html')
class TestElementWaitUntilNot(object):
    def test_returns_element_for_additional_actions(self, browser):
        element = browser.div(id='foo')
        browser.link(id='hide_foo').click()
        assert element.wait_until_not(lambda e: e.present) == element

    def test_accepts_self_by_default_in_wait_method(self, browser):
        element = browser.div(id='foo')
        browser.link(id='hide_foo').click()
        element.wait_until_not(lambda el: el.text == 'foo')

    def test_accepts_any_value_in_wait_method(self, browser):
        element = browser.div(id='foo')
        assert element.wait_until_not(lambda x: x == 'bar', object='foo')

    def test_accepts_just_a_timeout_parameter_with_method(self, browser):
        element = browser.div(id='foo')
        element.wait_until_not(timeout=0, method=lambda _: False)

    def test_accepts_just_a_message_parameter_with_method(self, browser):
        element = browser.div(id='foo')
        element.wait_until_not(message='no', method=lambda _: False)

    def test_accepts_just_an_interval_parameter_with_method(self, browser):
        element = browser.div(id='foo')
        element.wait_until_not(interval=0.1, method=lambda _: False)

    # Keyword

    @pytest.mark.usefixtures('refresh_before')
    def test_accepts_text_keyword(self, browser):
        element = browser.div(id='foo')
        browser.link(id='hide_foo').click()
        element.wait_until_not(text='foo')

    @pytest.mark.usefixtures('refresh_before')
    def test_accepts_regexp_value(self, browser):
        element = browser.div(id='foo')
        browser.link(id='hide_foo').click()
        element.wait_until_not(style=re.compile(r'block'))

    @pytest.mark.usefixtures('refresh_before')
    def test_accepts_multiple_keywords(self, browser):
        element = browser.div(id='foo')
        browser.link(id='hide_foo').click()
        element.wait_until_not(text='bar', style=re.compile(r'block'))

    @pytest.mark.usefixtures('refresh_before')
    def test_accepts_custom_attributes(self, browser):
        element = browser.div(id='foo')
        browser.link(id='hide_foo').click()
        element.wait_until_not(custom='')

    @pytest.mark.usefixtures('refresh_before')
    def test_accepts_keywords_and_methods(self, browser):
        element = browser.div(id='foo')
        browser.link(id='hide_foo').click()
        element.wait_until_not(lambda e: e.present, custom='')

    @pytest.mark.usefixtures('refresh_before')
    def test_browser_accepts_keywords(self, browser):
        browser.wait_until(title='wait test')
        with pytest.raises(TimeoutError):
            browser.wait_until(title='wrong')

    @pytest.mark.page('alerts.html')
    def test_alert_accepts_keywords(self, browser):
        try:
            browser.button(id='alert').click()
            browser.alert.wait_until(text='ok')
            with pytest.raises(TimeoutError):
                browser.alert.wait_until(text='not ok')
        finally:
            browser.alert.ok()

    @pytest.mark.usefixtures('refresh_before')
    def test_window_accepts_keywords(self, browser):
        browser.window().wait_until(title='wait test')
        with pytest.raises(TimeoutError):
            browser.window().wait_until(title='wrong')

    @pytest.mark.usefixtures('refresh_before', 'default_timeout_handling')
    def test_times_out_when_single_keyword_not_met(self, browser):
        element = browser.div(id='foo')
        with pytest.raises(TimeoutError):
            element.wait_until_not(id='foo')

    @pytest.mark.usefixtures('refresh_before', 'default_timeout_handling')
    def test_times_out_when_one_of_multiple_keywords_not_met(self, browser):
        element = browser.div(id='foo')
        browser.link(id='hide_foo').click()
        with pytest.raises(TimeoutError):
            element.wait_until_not(id='foo', style=re.compile(r'block'))

    @pytest.mark.usefixtures('refresh_before', 'default_timeout_handling')
    def test_times_out_when_a_custom_keyword_not_met(self, browser):
        element = browser.div(id='foo')
        with pytest.raises(TimeoutError):
            element.wait_until_not(custom='')


@pytest.mark.page('wait.html')
@pytest.mark.usefixtures('refresh_before')
@pytest.mark.usefixtures('default_timeout_handling')
class TestElementPresenceReadOnlyEnabled(object):

    def test_raises_exception_on_element_never_present_after_timing_out(self, browser):
        element = browser.link(id='not_there')
        with pytest.raises(UnknownObjectException):
            element.click()

    def test_does_not_wait_when_acting_on_an_element_already_present(self, browser):
        result, duration = executed_within(browser.link().click, max=1)
        assert result, f'Waited longer than 1 second to act on element! ({duration})'

    def test_waits_until_element_present_when_acting_on_element_becomes_present(self, browser):
        def func():
            browser.link(id='show_bar').click()
            browser.div(id='bar').click()

        result, duration = executed_within(func, min=1)
        assert result, f'Element was not acted upon between 1 and 2 seconds! ({duration})'
        assert browser.div(id='bar').text == 'changed'

    def test_waits_until_text_field_present_when_acting_on_element_becomes_present(self, browser):
        def func():
            browser.link(id='show_textfield').click()
            browser.textfield(id='textfield').set('Foo')

        result, duration = executed_within(func, min=1)
        assert result, f'Element was not acted upon between 1 and 2 seconds! ({duration})'

    # ReadOnly

    def test_raises_exception_on_read_only_text_field_never_becomes_writable(self, browser):
        with pytest.raises(ObjectReadOnlyException):
            browser.text_field(id='writable').set('foo')

    def test_waits_until_writable(self, browser):
        def func():
            browser.link(id='make-writable').click()
            browser.text_field(id='writable').set('foo')

        result, duration = executed_within(func, min=1)
        assert result, f'Element was not acted upon between 1 and 2 seconds! ({duration})'

    # Enabled

    def test_raises_exception_on_read_only_text_field_never_becomes_enabled(self, browser):
        with pytest.raises(ObjectDisabledException):
            browser.button(id='btn').click()

    def test_waits_until_enabled(self, browser):
        def func():
            browser.link(id='enable_btn').click()
            browser.button(id='btn').click()

        result, duration = executed_within(func, min=1)
        assert result, f'Element was not acted upon between 1 and 2 seconds! ({duration})'

    # Parent

    def test_raises_exception_on_parent_never_present(self, browser):
        element = browser.link(id='not_there')
        with pytest.raises(UnknownObjectException):
            element.element.click()

    @pytest.mark.usefixtures('default_timeout_handling')
    def test_raises_exception_on_element_from_collection_parent_never_present(self, browser):
        element = browser.link(id='not_there')
        with pytest.raises(UnknownObjectException):
            element.elements[2].click()

    @pytest.mark.usefixtures('default_timeout_handling')
    def test_does_not_wait_for_element_to_be_present_when_querying_child_element(self, browser):
        def func():
            el = browser.element(id='not_there').element(id='doesnt_matter')
            el.present

        result, duration = executed_within(func, max=1)
        assert result, f'Element was not acted upon between 1 and 2 seconds! ({duration})'


@pytest.mark.page('wait.html')
@pytest.mark.usefixtures('refresh_before')
@pytest.mark.usefixtures('default_timeout_handling')
class TestElementCollectionUntil():

    def test_returns_collection(self, browser):
        elements = browser.divs()
        assert elements.wait_until(lambda _: elements.exist) == elements

    def test_times_out_when_waiting_for_non_empty_collection(self, browser):
        divs = browser.divs()
        with pytest.raises(TimeoutError):
            divs.wait_until(lambda d: d.is_empty)

    def test_provides_matching_collection_when_exists(self, browser):
        def func():
            browser.link(id='add_foobar').click()
            browser.divs(id='foobar').wait_until(lambda d: d.exists)

        result, duration = executed_within(func, min=1)
        assert result, f'Collection was not found between 1 and 2 seconds! ({duration})'

    def test_accepts_self_in_lambda(self, browser):
        def func():
            browser.link(id='add_foobar').click()
            browser.divs().wait_until(lambda d: len(d) == 7)

        result, duration = executed_within(func, min=1)
        assert result, f'Collection was not found between 1 and 2 seconds! ({duration})'

    def test_waits_for_parent_element_to_be_present_before_locating(self, browser):
        els = browser.element(id=re.compile(r'not|there')).elements(id='doesnt_matter')
        with pytest.raises(UnknownObjectException):
            list(els)

    def test_accepts_attributes_to_evaluate(self, browser):
        def func():
            browser.link(id='add_foobar').click()
            browser.divs().wait_until(size=7)

        result, duration = executed_within(func, min=1)
        assert result, f'Collection was not found between 1 and 2 seconds! ({duration})'


@pytest.mark.page('wait.html')
@pytest.mark.usefixtures('refresh_before')
@pytest.mark.usefixtures('default_timeout_handling')
class TestElementCollectionUntilNot():

    def test_returns_collection(self, browser):
        elements = browser.divs()
        assert elements.wait_until_not(lambda _: elements.is_empty) == elements

    def test_times_out_when_waiting_for_non_empty_collection(self, browser):
        divs = browser.divs()
        with pytest.raises(TimeoutError):
            divs.wait_until_not(lambda d: d.exists)

    def test_provides_matching_collection_when_not_exists(self, browser):
        def func():
            browser.link(id='remove_foo').click()
            browser.divs(id='foo').wait_until_not(lambda d: d.exists)

        result, duration = executed_within(func, min=1)
        assert result, f'Collection was not found between 1 and 2 seconds! ({duration})'

    def test_accepts_self_in_lambda(self, browser):

        def func():
            browser.link(id='add_foobar').click()
            browser.divs().wait_until_not(lambda d: len(d) == 6)

        result, duration = executed_within(func, min=1)
        assert result, f'Collection was not found between 1 and 2 seconds! ({duration})'
