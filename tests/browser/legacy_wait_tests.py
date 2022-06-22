from time import time

import pytest

import nerodia
from nerodia.exception import UnknownObjectException
from nerodia.wait.wait import TimeoutError, Wait


@pytest.mark.skipif('not nerodia.relaxed_locate',
                    reason='only applicable when relaxed locating')
@pytest.mark.page('wait.html')
class TestElementWaitUntilPresent(object):
    def test_waits_until_the_element_appears(self, browser):
        browser.link(id='show_bar').click()
        browser.div(id='bar').wait_until_present(timeout=5)

    def test_waits_until_the_element_reappears(self, browser):
        browser.link(id='readd_bar').click()
        browser.div(id='bar').wait_until_present()

    def test_times_out_if_the_element_doesnt_appear(self, browser):
        message_parts = ['timed out after 1 seconds, waiting for ',
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


@pytest.mark.skipif('not nerodia.relaxed_locate',
                    reason='only applicable when relaxed locating')
@pytest.mark.page('wait.html')
class TestElementWaitUntilNotPresent(object):
    def test_waits_until_the_element_disappears(self, browser):
        browser.link(id='hide_foo').click()
        browser.div(id='foo').wait_until_not_present(timeout=2)

    def test_times_out_if_the_element_doesnt_disappear(self, browser):
        message_parts = ['timed out after 1 seconds, waiting for ',
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
        element = browser.div(id='foo').locate()

        browser.link(id='hide_foo').click()
        element.wait_until_not_present(timeout=1)

    @pytest.mark.usefixtures('default_timeout_handling')
    def test_waits_until_the_selector_no_longer_matches(self, browser):
        element = browser.link(name='add_select').wait_until(lambda x: x.exists)
        browser.link(id='change_select').click()
        element.wait_until_not_present()


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
@pytest.mark.usefixtures('timeout_reset')
@pytest.mark.skipif('nerodia.relaxed_locate',
                    reason='only applicable when not relaxed locating')
class TestNotRelaxedLocate(object):
    def test_raises_exception_immediately_on_element_never_present(self, browser):
        timeout = 2
        nerodia.default_timeout = timeout
        element = browser.link(id='not_there')
        with pytest.raises(UnknownObjectException):
            start = time()
            element.click()
        assert time() - start < 1

    def test_raises_exception_immediately_on_element_eventually_present(self, browser):
        from selenium.common.exceptions import ElementNotInteractableException, \
            ElementNotVisibleException
        err = ElementNotInteractableException if browser.name == 'firefox' \
            else ElementNotVisibleException
        nerodia.default_timeout = 3
        browser.link(id='show_bar').click()
        with pytest.raises(err):
            browser.div(id='bar').click()
