from time import time

import pytest

import nerodia
from nerodia.exception import UnknownObjectException


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

    def test_raises_exception_after_timing_out_on_element_parent_never_present(self, browser):
        timeout = 2
        nerodia.default_timeout = timeout
        with pytest.raises(UnknownObjectException):
            element = browser.link(id='not_there')
            start = time()
            element.element().click()
        assert time() - start > timeout

    def test_raises_exception_after_timing_out_on_element_from_collection_parent_never_present(self, browser):
        timeout = 2
        nerodia.default_timeout = timeout
        with pytest.raises(UnknownObjectException):
            element = browser.link(id='not_there')
            start = time()
            element.elements()[2].click()
        assert time() - start > timeout

    def test_does_not_wait_on_element_that_is_already_present(self, browser):
        nerodia.default_timeout = 5
        element = browser.link()
        start = time()
        element.click()
        assert time() - start < 5

    def test_waits_until_present_present_and_takes_action_on_element_eventually_present(self, browser):
        nerodia.default_timeout = 3
        element = browser.link(id='show_bar')
        start = time()
        element.click()
        assert time() - start < 3

    def test_ensures_all_checks_happen_once_even_if_time_has_expired(self, browser):
        nerodia.default_timeout = -1
        browser.link().click()


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
