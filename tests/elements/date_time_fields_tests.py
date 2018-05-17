import pytest

from nerodia.elements.date_time_field import DateTimeField

pytestmark = pytest.mark.page('forms_with_input_elements.html')


def test_returns_the_matching_elements(browser):
    assert list(browser.date_time_fields(name='html5_datetime-local')) == \
        [browser.date_time_field(name='html5_datetime-local')]


def test_returns_the_number_of_date_time_fields(browser):
    assert len(browser.date_time_fields()) == 1


def test_returns_the_date_time_field_at_the_given_index(browser):
    assert browser.date_time_fields()[0].id == 'html5_datetime-local'


def test_iterates_through_date_time_fields_correctly(browser):
    count = 0
    for index, d in enumerate(browser.date_time_fields()):
        date_time_field = browser.date_time_field(index=index)
        assert isinstance(d, DateTimeField)
        assert d.name == date_time_field.name
        assert d.id == date_time_field.id
        assert d.value == date_time_field.value
        count += 1
    assert count > 0
