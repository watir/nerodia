import re

import pytest


@pytest.mark.page('wait.html')
class TestElementVisible(object):
    def test_finds_single_element(self, browser):
        assert browser.body().element(visible=True).id == 'foo'

    def test_handles_tag_name_and_index(self, browser):
        assert browser.div(visible=True, index=1).id == 'buttons'

    def test_handles_tag_name_and_a_single_regexp_attribute(self, browser):
        assert browser.div(visible=True, id=re.compile(r'ons')).id == 'buttons'

    def test_handles_xpath(self, browser):
        assert browser.element(visible=True, xpath='.//div[@id="foo"]').id == 'foo'

    def test_handles_css(self, browser):
        assert browser.element(visible=True, css='div#foo').id == 'foo'

    def test_handles_collections(self, browser):
        assert len(browser.divs(visible=True)) == 3


@pytest.mark.page('wait.html')
class TestElementHidden(object):
    def test_finds_single_element(self, browser):
        assert browser.body().element(visible=False).id == 'bar'

    def test_handles_tag_name_and_index(self, browser):
        assert browser.div(visible=False, index=1).id == 'also_hidden'

    def test_handles_tag_name_and_a_single_regexp_attribute(self, browser):
        assert browser.div(visible=False, id=re.compile(r'_')).id == 'also_hidden'

    def test_handles_xpath(self, browser):
        assert browser.element(visible=False, xpath='.//div[@id="bar"]').id == 'bar'

    def test_handles_css(self, browser):
        assert browser.element(visible=False, css='div#bar').id == 'bar'

    def test_handles_collections(self, browser):
        assert len(browser.divs(visible=False)) == 3

    def test_raises_exception_when_value_is_not_boolean(self, browser):
        msg = "expected one of {!r}, got 'true':{}".format([bool], str)
        with pytest.raises(TypeError) as e:
            browser.body().element(visible='true')
        assert e.value.args[0] == msg
