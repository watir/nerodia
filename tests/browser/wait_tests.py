import re
from time import time

import pytest

import nerodia
from nerodia.exception import UnknownObjectException, ObjectDisabledException
from nerodia.wait.wait import Wait, TimeoutError


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


@pytest.mark.skipif('not nerodia.relaxed_locate', reason='only applicable when relaxed locating')
@pytest.mark.page('wait.html')
class TestAutomaticWait(object):
    def test_clicking_automatically_waits_until_the_element_appears(self, browser):
        browser.link(id='show_bar').click()
        browser.div(id='bar').click()
        assert browser.div(id='bar').text == 'changed'

    def test_raises_exception_if_the_element_doesnt_appear(self, browser):
        with pytest.raises(UnknownObjectException):
            browser.div(id='bar').click()

    @pytest.mark.usefixtures('quick_timeout')
    def test_raises_exception_if_the_element_doesnt_become_enabled(self, browser):
        with pytest.raises(ObjectDisabledException):
            browser.button(id='btn').click()


@pytest.mark.skipif('nerodia.relaxed_locate',
                    reason='only applicable when not relaxed locating')
@pytest.mark.page('wait.html')
class TestElementWaitUntilEnabled(object):
    def test_invokes_subsequent_method_calls_when_the_element_becomes_enabled(self, browser):
        browser.link(id='enable_btn').click()

        btn = browser.button(id='btn')
        btn.wait_until(timeout=2, method=lambda b: b.enabled).click()
        Wait.until_not(lambda: btn.enabled)
        assert btn.disabled

    def test_invokes_subsequent_method_calls_when_the_element_becomes_enabled_with_alias(self, browser):
        browser.link(id='enable_btn').click()

        btn = browser.button(id='btn')
        btn.wait_until(timeout=2, method=lambda b: b.enabled).click()
        Wait.whilst(lambda: btn.enabled)
        assert btn.disabled

    def test_times_out(self, browser):
        message_parts = ['timed out after 1 seconds, waiting for true condition on',
                         '#<Button: located: True;', "'tag_name': 'button'", "'id': 'btn'"]
        element = browser.button(id='btn')
        with pytest.raises(TimeoutError) as e:
            element.wait_until(timeout=1, method=lambda e: e.enabled).click()
        assert all(part in e.value.args[0] for part in message_parts)

    def test_responds_to_element_methods(self, browser):
        element = browser.button().wait_until(method=lambda _: True)

        assert hasattr(element, 'exist')
        assert hasattr(element, 'present')
        assert hasattr(element, 'click')

    def test_can_be_chained_with_wait_until_present(self, browser):
        browser.link(id='show_and_enable_btn').click()
        browser.button(id='btn2').wait_until(lambda b: b.present).wait_until(
            lambda b: b.enabled).click()

        assert browser.button(id='btn2').exists
        assert browser.button(id='btn2').enabled


@pytest.mark.page('wait.html')
class TestElementWaitUntilPresent(object):
    def test_waits_until_the_element_appears(self, browser):
        browser.link(id='show_bar').click()
        browser.div(id='bar').wait_until_present(timeout=5)

    def test_waits_until_the_element_reappears(self, browser):
        browser.link(id='readd_bar').click()
        browser.div(id='bar').wait_until_present()

    def test_times_out_if_the_element_doesnt_appear(self, browser):
        message_parts = ['timed out after 1 seconds, waiting for element',
                         '#<Div: located: True;', "'id': 'bar'", "'tag_name': 'div'",
                         'to become present']
        with pytest.raises(TimeoutError) as e:
            browser.div(id='bar').wait_until_present(timeout=1)
        assert all(part in e.value.args[0] for part in message_parts)

    def test_users_provided_interval(self, browser, mocker):
        mock = mocker.patch('nerodia.elements.html_elements.Div.present',
                            new_callable=mocker.PropertyMock)
        element = browser.div(id='bar')
        try:
            element.wait_until_present(timeout=0.4, interval=0.2)
        except TimeoutError:
            pass
        assert mock.call_count == 2


@pytest.mark.page('wait.html')
class TestElementWaitUntilNotPresent(object):
    def test_waits_until_the_element_disappears(self, browser):
        browser.link(id='hide_foo').click()
        browser.div(id='foo').wait_until_not_present(timeout=2)

    def test_times_out_if_the_element_doesnt_disappear(self, browser):
        message_parts = ['timed out after 1 seconds, waiting for element',
                         '#<Div: located: True;', "'tag_name': 'div'", "'id': 'foo'",
                         'not to be present']
        with pytest.raises(TimeoutError) as e:
            browser.div(id='foo').wait_until_not_present(timeout=1)
        assert all(part in e.value.args[0] for part in message_parts)

    def test_users_provided_interval(self, browser, mocker):
        mock = mocker.patch('nerodia.elements.html_elements.Div.present',
                            new_callable=mocker.PropertyMock)
        element = browser.div(id='foo')
        try:
            element.wait_until_not_present(timeout=0.4, interval=0.2)
        except TimeoutError:
            pass
        assert mock.call_count == 2

    def test_does_not_error_when_element_goes_stale(self, browser):
        element = browser.div(id='foo')
        element.exists

        browser.link(id='hide_foo').click()
        element.wait_until_not_present(timeout=1)

    @pytest.mark.usefixtures('default_timeout_handling')
    def test_waits_until_the_selector_no_longer_matches(self, browser):
        element = browser.link(name='add_select').wait_until(lambda x: x.exists)
        browser.link(id='change_select').click()
        element.wait_until_not_present()


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
    def test_accepts_custom_keyword(self, browser):
        element = browser.div(id='foo')
        browser.link(id='hide_foo').click()
        element.wait_until_not(custom='bar')

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

    def test_is_used_by_element_wait_until_present(self, browser):
        start_time = time()
        with pytest.raises(TimeoutError):
            browser.div(id='bar').wait_until_present()
        assert nerodia.default_timeout < time() - start_time < nerodia.default_timeout + 1

    def test_is_used_by_element_wait_until_not_present(self, browser):
        start_time = time()
        with pytest.raises(TimeoutError):
            browser.div(id='foo').wait_until_not_present()
        assert nerodia.default_timeout < time() - start_time < nerodia.default_timeout + 1
