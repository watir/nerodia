import pytest


@pytest.mark.page('special_chars.html')
def test_finds_elements_with_single_quotes(browser):
    assert browser.div(text="single 'quotes'").exists
