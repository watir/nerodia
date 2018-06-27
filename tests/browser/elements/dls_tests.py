import pytest

pytestmark = pytest.mark.page('definition_lists.html')


def test_returns_the_matching_elements(browser):
    assert list(browser.dls(title='experience')) == [browser.dl(title='experience')]


def test_returns_the_number_of_divs(browser):
    assert len(browser.dls()) == 3


def test_returns_the_dl_at_the_given_index(browser):
    assert browser.dls()[0].id == 'experience-list'


def test_iterates_through_dls_correctly(browser):
    count = 0
    for index, d in enumerate(browser.dls()):
        dl = browser.dl(index=index)
        assert d.id == dl.id
        assert d.class_name == dl.class_name
        count += 1
    assert count > 0
