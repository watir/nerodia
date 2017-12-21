import pytest

pytestmark = pytest.mark.page('non_control_elements.html')


def test_returns_the_matching_elements(browser):
    assert browser.divs(id='header').to_list == [browser.div(id='header')]


def test_returns_the_number_of_divs(browser):
    assert len(browser.divs()) == 16


def test_returns_the_div_at_the_given_index(browser):
    assert browser.divs()[1].id == 'outer_container'


def test_iterates_through_divs_correctly(browser):
    count = 0
    for index, d in enumerate(browser.divs()):
        div = browser.div(index=index)
        assert d.id == div.id
        assert d.class_name == div.class_name
        count += 1
    assert count > 0
