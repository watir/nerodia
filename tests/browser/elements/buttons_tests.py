import pytest

pytestmark = pytest.mark.page('forms_with_input_elements.html')


def test_returns_the_matching_elements(browser):
    assert list(browser.buttons(name='new_user_button')) == [
        browser.button(name='new_user_button')]


def test_returns_the_number_of_buttons(browser):
    assert len(browser.buttons()) == 11


def test_returns_the_button_at_the_given_index(browser):
    assert browser.buttons()[0].title == 'Submit the form'


def test_iterates_through_buttons_correctly(browser):
    count = 0
    for index, b in enumerate(browser.buttons()):
        button = browser.button(index=index)
        assert b.name == button.name
        assert b.id == button.id
        assert b.value == button.value
        count += 1
    assert count > 0
