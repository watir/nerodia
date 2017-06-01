from time import time

import pytest

import nerodia
from nerodia.exception import UnknownObjectException, ObjectDisabledException, \
    ObjectReadOnlyException


@pytest.fixture
def timeout_reset():
    original = nerodia.default_timeout
    yield
    nerodia.default_timeout = original


@pytest.mark.page('wait.html')
@pytest.mark.usefixtures('timeout_reset')
@pytest.mark.skipif('nerodia.relaxed_locate is False',
                    reason='only applicable when relaxed locating')
class TestRelaxedLocate(object):
    def test_raises_exception_after_timing_out_on_element_never_present(self, browser):
        timeout = 2
        nerodia.default_timeout = timeout
        with pytest.raises(UnknownObjectException):
            element = browser.link(id='not_there')
            start = time()
            element.click()
        assert time() - start > timeout

    def test_does_not_wait_on_element_that_is_already_present(self, browser):
        nerodia.default_timeout = 2
        element = browser.link()
        start = time()
        element.click()
        assert time() - start < 2

    def test_waits_until_present_present_and_takes_action_on_element_eventually_present(self, browser):
        nerodia.default_timeout = 3
        element = browser.link(id='show_bar')
        start = time()
        element.click()
        assert time() - start < 3

    # failure_precedence

    def test_fails_first_for_parent_not_existing(self, browser):
        nerodia.default_timeout = 0
        repr = "#<Div: located: False; {'tag_name': 'div', 'id': 'no_parent'}>"
        msg = "timed out after {} seconds, waiting for {} to be " \
              "located".format(nerodia.default_timeout, repr)
        with pytest.raises(UnknownObjectException) as e:
            element = browser.div(id='no_parent').div(id='no_child')
            element.click()
        assert e.value.message == msg

    def test_fails_for_child_not_existing_if_parent_exists(self, browser):
        nerodia.default_timeout = 0
        repr = "#<Div: located: False; {'tag_name': 'div', 'id': 'buttons'} --> " \
               "{'tag_name': 'div', 'id': 'no_child'}>"
        msg = "timed out after {} seconds, waiting for {} to be " \
              "located".format(nerodia.default_timeout, repr)
        with pytest.raises(UnknownObjectException) as e:
            element = browser.div(id='buttons').div(id='no_child')
            element.click()
        assert e.value.message == msg

    def test_fails_for_parent_not_present_if_child_exists(self, browser):
        nerodia.default_timeout = 0
        repr = "#<Div: located: True; {'tag_name': 'div', 'id': 'also_hidden'}>"
        msg = "timed out after {} seconds, waiting for {} to be " \
              "located".format(nerodia.default_timeout, repr)
        with pytest.raises(UnknownObjectException) as e:
            element = browser.div(id='also_hidden').div(id='hidden_child')
            element.click()
        assert e.value.message == msg

    def test_fails_for_parent_not_present_if_parent_is_present(self, browser):
        nerodia.default_timeout = 0
        repr = "#<Button: located: True; {'tag_name': 'div', 'id': 'buttons'} --> " \
               "{'tag_name': 'button', 'id': 'btn2'}>"
        msg = "timed out after {} seconds, waiting for {} to be " \
              "located".format(nerodia.default_timeout, repr)
        with pytest.raises(UnknownObjectException) as e:
            element = browser.div(id='buttons').button(id='btn2')
            element.click()
        assert e.value.message == msg

    @pytest.mark.page('forms_with_input_elements.html')
    def test_fails_for_element_not_enabled_if_present(self, browser):
        nerodia.default_timeout = 0
        repr = "#<TextField: located: True; {'tag_name': 'form', 'id': 'new_user'} --> " \
               "{'tag_name': 'input or textarea', 'type': '(any text type)', 'id': 'good_luck'}>"
        msg = "element present, but timed out after {} seconds, waiting for {} to be " \
              "enabled".format(nerodia.default_timeout, repr)
        with pytest.raises(ObjectDisabledException) as e:
            element = browser.form(id='new_user').text_field(id='good_luck')
            element.set('foo')
        assert e.value.message == msg

    @pytest.mark.page('forms_with_input_elements.html')
    def test_fails_for_element_not_being_readonly_if_enabled(self, browser):
        nerodia.default_timeout = 0.5
        repr = "#<TextField: located: True; {'tag_name': 'form', 'id': 'new_user'} --> " \
               "{'tag_name': 'input or textarea', 'type': '(any text type)', 'id': 'new_user_code'}>"
        msg = "element present and enabled, but timed out after {} seconds, waiting for {} to " \
              "not be readonly".format(nerodia.default_timeout, repr)
        with pytest.raises(ObjectReadOnlyException) as e:
            element = browser.form(id='new_user').text_field(id='new_user_code')
            element.set('foo')
        assert e.value.message == msg

    def test_gives_warning_when_catching_for_flow_control(self, browser):
        from .support import captured_output
        nerodia.default_timeout = 1
        msg = 'This code has slept for the duration of the default timeout waiting for an ' \
              'Element to exist. If the test is still passing, consider using Element#exists ' \
              'instead of catching UnknownObjectException\n'
        with captured_output() as (out, err):
            try:
                element = browser.link(id='not_there')
                element.click()
            except UnknownObjectException:
                pass

            assert msg in err.getvalue().strip()

    def test_ensures_all_checks_happen_once_even_if_time_has_expired(self, browser):
        nerodia.default_timeout = -1
        browser.link().click()

    def test_ensures_the_same_timeout_is_used_for_all_of_the_calls(self, browser):
        nerodia.default_timeout = 1.1
        browser.link(id='add_foobar').click()
        # Element created after 1 second, and displays after 2 seconds
        # Click will only raise this exception if the timer is not reset between #wait_for_exists and #wait_for_present
        with pytest.raises(UnknownObjectException):
            browser.div(id='foobar').click()


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
        from selenium.common.exceptions import ElementNotVisibleException
        nerodia.default_timeout = 3
        browser.link(id='show_bar').click()
        with pytest.raises(ElementNotVisibleException):
            browser.div(id='bar').click()
