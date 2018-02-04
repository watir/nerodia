import pytest

from nerodia.elements.date_field import DateField

pytestmark = pytest.mark.page('forms_with_input_elements.html')


def test_returns_the_matching_elements(browser):
    assert browser.date_fields(name='html5_date').to_list == [browser.date_field(name='html5_date')]


def test_returns_the_number_of_date_fields(browser):
    assert len(browser.date_fields()) == 1


def test_returns_the_date_field_at_the_given_index(browser):
    assert browser.date_fields()[0].id == 'html5_date'


def test_iterates_through_date_fields_correctly(browser):
    count = 0
    for index, d in enumerate(browser.date_fields()):
        date_field = browser.date_field(index=index)
        assert isinstance(d, DateField)
        assert d.name == date_field.name
        assert d.id == date_field.id
        assert d.value == date_field.value
        count += 1
    assert count > 0
