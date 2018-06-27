from re import compile

import pytest

pytestmark = pytest.mark.page('forms_with_input_elements.html')


class TestTextAreasByValue(object):
    def test_finds_textareas_by_string(self, browser):
        browser.textarea(index=0).set('foo1')
        browser.textarea(index=1).set('foo2')
        assert [e.id for e in browser.textareas(value='foo1')] == [browser.textarea(index=0).id]
        assert [e.id for e in browser.textareas(value='foo2')] == [browser.textarea(index=1).id]

    def test_finds_textareas_by_regexp(self, browser):
        browser.textarea(index=0).set('foo1')
        browser.textarea(index=1).set('foo2')
        assert browser.textareas(value=compile(r'foo'))[0].id == browser.textarea(index=0).id
        assert browser.textareas(value=compile(r'foo'))[1].id == browser.textarea(index=1).id
