import pytest

pytestmark = pytest.mark.page('images.html')


def test_returns_the_matching_elements(browser, page):
    assert browser.areas(alt="Tables").to_list == [browser.area(alt="Tables")]


def test_returns_the_number_of_areas(browser, page):
    assert len(browser.areas()) == 3


def test_returns_the_area_at_the_given_index(browser, page):
    assert browser.areas()[0].id == 'NCE'


def test_iterates_through_areas_correctly(browser, page):
    count = 0
    for index, a in enumerate(browser.areas()):
        assert a.id == browser.area(index=index).id
        assert a.title == browser.area(index=index).title
        count += 1
    assert count > 0
