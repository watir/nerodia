import pytest

pytestmark = pytest.mark.page('forms_with_input_elements.html')


class TestMeta(object):
    def test_returns_true_if_the_element_exists(self, browser):
        assert browser.meta(http_equiv='Content-Type').exists is True

    def test_returns_the_first_meta_if_given_no_args(self, browser):
        assert browser.meta().exists

    def test_returns_the_content_attribute_of_the_tag(self, browser):
        assert browser.meta(http_equiv='Content-Type').content == "text/html; charset=utf-8"
