from re import compile

import pytest

pytestmark = pytest.mark.page('forms_with_input_elements.html')


class TestTextArea(object):
    def test_can_set_a_value(self, browser):
        browser.textarea().set('foo')
        assert browser.textarea().value == 'foo'

    def test_can_clear_a_value(self, browser):
        browser.textarea().set('foo')
        browser.textarea().clear()
        assert browser.textarea().value == ''

    def test_locates_textarea_by_value(self, browser):
        browser.textarea().set('foo')
        assert browser.textarea(value=compile(r'foo')).exists
        assert browser.textarea(value='foo').exists
