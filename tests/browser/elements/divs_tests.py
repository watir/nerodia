import pytest

pytestmark = pytest.mark.page('non_control_elements.html')


def test_returns_the_matching_elements(browser):
    assert list(browser.divs(id='header')) == [browser.div(id='header')]


def test_returns_the_number_of_divs(browser):
    assert len(browser.divs()) == 16


def test_returns_the_div_at_the_given_index(browser):
    assert browser.divs()[1].id == 'outer_container'


def test_returns_a_list_of_divs_with_a_given_slice_of_positive_values(browser):
    divs = browser.divs()[2:5]
    ids = [_.id for _ in divs]
    assert ids == ['header', 'promo', 'content']


def test_returns_a_list_of_divs_with_a_given_slice_including_negative_values(browser):
    divs = browser.divs()[11:-2]
    ids = [_.id for _ in divs]
    assert ids == ['messages', 'ins_tag_test', 'del_tag_test']


def test_iterates_through_divs_correctly(browser):
    count = 0
    for index, d in enumerate(browser.divs()):
        div = browser.div(index=index)
        assert d.id == div.id
        assert d.class_name == div.class_name
        count += 1
    assert count > 0
