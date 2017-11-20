from time import time

import pytest

import nerodia
from nerodia.exception import NoValueFoundException
from nerodia.wait.wait import Wait, TimeoutError, Timer


@pytest.fixture
def default_timeout_handling(browser):
    orig_timeout = nerodia.default_timeout
    nerodia.default_timeout = 1
    yield
    nerodia.default_timeout = orig_timeout


class TestWaitUntil(object):
    # until

    def test_waits_until_the_method_returns_true(self):
        assert Wait.until(timeout=0.5, method=lambda: True)

    def test_exeuctes_method_if_timeout_is_zero(self):
        assert Wait.until(timeout=0, method=lambda: True)

    def test_times_out(self):
        with pytest.raises(TimeoutError):
            Wait.until(timeout=0.5, method=lambda: False)

    def test_times_out_with_a_custom_message(self):
        msg = 'oops'
        with pytest.raises(TimeoutError) as e:
            Wait.until(timeout=0.5, message=msg, method=lambda: False)
        assert e.value.message == 'timed out after 0.5 seconds, {}'.format(msg)

    def test_uses_provided_interval(self):
        count = {'value': 0}

        def method():
            count['value'] += 1

        try:
            Wait.until(timeout=0.4, interval=0.2, method=method)
        except TimeoutError:
            pass
        assert count.get('value') == 2

    def test_uses_timer_for_waiting(self, mocker):
        mocker.patch('nerodia.wait.wait.Timer.wait')
        Wait.until(timeout=0.5, method=lambda: True)
        Timer.wait.assert_called_once()


class TestWaitWhile(object):
    # until_not

    def test_waits_while_the_method_returns_true(self):
        assert Wait.until_not(timeout=0.5, method=lambda: False)

    def test_exeuctes_method_if_timeout_is_zero(self):
        assert Wait.until_not(timeout=0, method=lambda: False)

    def test_times_out(self):
        with pytest.raises(TimeoutError):
            Wait.until_not(timeout=0.5, method=lambda: True)

    def test_times_out_with_a_custom_message(self):
        msg = 'oops'
        with pytest.raises(TimeoutError) as e:
            Wait.until_not(timeout=0.5, message=msg, method=lambda: True)
        assert e.value.message == 'timed out after 0.5 seconds, {}'.format(msg)

    def test_uses_provided_interval(self):
        count = {'value': 0}

        def method():
            count['value'] += 1

        try:
            Wait.until_not(timeout=0.4, interval=0.2, method=method)
        except TimeoutError:
            pass
        assert count.get('value') == 2

    def test_uses_timer_for_waiting(self, mocker):
        mocker.patch('nerodia.wait.wait.Timer.wait')
        Wait.until_not(timeout=0.5, method=lambda: True)
        Timer.wait.assert_called_once()


class TestWaitDefaultTimer(object):
    def test_returns_default_timer(self):
        assert isinstance(Wait.timer, Timer)

    def test_changes_default_timer(self):
        class Foo():
            pass
        try:
            timer = Foo()
            Wait.timer = timer
            assert Wait.timer == timer
        finally:
            Wait.timer = Timer()


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

    def test_times_out(self, browser):
        repr = "#<Button: located: False; {'tag_name': 'button', 'id': 'btn'}>"
        message = 'timed out after 1 seconds, waiting for true condition on {}'.format(repr)
        element = browser.button(id='btn')
        with pytest.raises(TimeoutError) as e:
            element.wait_until(timeout=1, method=lambda e: e.enabled).click()
        assert e.value.message == message

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

    def test_times_out_if_the_element_doesnt_appear(self, browser):
        message = 'timed out after 1 seconds, waiting for true condition on present'
        with pytest.raises(TimeoutError) as e:
            browser.div(id='bar').wait_until_present(timeout=1)
        assert e.value.message == message

    def test_users_provided_interval(self, browser, mocker):
        mock = mocker.patch('nerodia.elements.html_elements.Div.present',
                            new_callable=mocker.PropertyMock)
        element = browser.div(id='bar')
        try:
            element.wait_until_present(timeout=0.4, interval=0.2)
        except TimeoutError:
            pass
        assert mock.call_count == 2

    @pytest.mark.usefixtures('default_timeout_handling')
    def test_waits_to_select_an_option(self, browser):
        browser.link(id='add_select').click()
        select_list = browser.select_list(id='languages')
        start_time = time()
        with pytest.raises(NoValueFoundException):
            select_list.select('No')
        assert time() - start_time > 1


@pytest.mark.page('wait.html')
class TestElementWaitUntilNotPresent(object):
    def test_waits_until_the_element_disappears(self, browser):
        browser.link(id='hide_foo').click()
        browser.div(id='foo').wait_until_not_present(timeout=2)

    def test_times_out_if_the_element_doesnt_disappear(self, browser):
        element = "#<Div: located: False;"
        tag = "'tag_name': 'div'"
        id = "'id': 'foo'"
        message = 'timed out after 1 seconds, waiting for false condition on'
        with pytest.raises(TimeoutError) as e:
            browser.div(id='foo').wait_until_not_present(timeout=1)
        assert element in e.value.message
        assert tag in e.value.message
        assert id in e.value.message
        assert message in e.value.message

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
