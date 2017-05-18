import pytest


@pytest.mark.page('forms_with_input_elements.html')
class TestInputType(object):
    def test_returns_an_email_type(self, browser):
        assert browser.input(name='html5_email').type == 'email'
