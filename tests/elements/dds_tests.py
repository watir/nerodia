import pytest

pytestmark = pytest.mark.page('definition_lists.html')


def test_returns_the_matching_elements(browser):
    assert list(browser.dds(text='11 years')) == [browser.dd(text='11 years')]


def test_returns_the_number_of_dds(browser):
    assert len(browser.dds()) == 11


def test_returns_the_dd_at_the_given_index(browser):
    assert browser.dds()[1].title == 'education'


def test_iterates_through_dds_correctly(browser):
    count = 0
    for index, d in enumerate(browser.dds()):
        dd = browser.dd(index=index)
        assert d.id == dd.id
        assert d.class_name == dd.class_name
        count += 1
    assert count > 0
