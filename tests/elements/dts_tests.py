import pytest

pytestmark = pytest.mark.page('definition_lists.html')


def test_returns_the_matching_elements(browser):
    assert browser.dts(class_name='current-industry').to_list == \
        [browser.dt(class_name='current-industry')]


def test_returns_the_number_of_divs(browser):
    assert len(browser.dts()) == 11


def test_returns_the_dt_at_the_given_index(browser):
    assert browser.dts()[0].id == 'experience'


def test_iterates_through_dts_correctly(browser):
    count = 0
    for index, d in enumerate(browser.dts()):
        dt = browser.dt(index=index)
        assert d.id == dt.id
        assert d.class_name == dt.class_name
        count += 1
    assert count > 0
