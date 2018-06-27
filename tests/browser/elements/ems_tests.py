import pytest

pytestmark = pytest.mark.page('non_control_elements.html')


def test_returns_the_matching_elements(browser):
    assert list(browser.ems(class_name='important-class')) == [
        browser.em(class_name='important-class')]


def test_returns_the_number_of_ems(browser):
    assert len(browser.ems()) == 1


def test_returns_the_div_at_the_given_index(browser):
    assert browser.ems()[0].id == 'important-id'


def test_iterates_through_ems_correctly(browser):
    count = 0
    for index, e in enumerate(browser.ems()):
        em = browser.em(index=index)
        assert e.id == em.id
        assert e.class_name == em.class_name
        count += 1
    assert count > 0
