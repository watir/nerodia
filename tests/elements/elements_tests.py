import pytest

from re import compile

pytestmark = pytest.mark.page('forms_with_input_elements.html')


# get_item
def test_returns_not_existing_element_when_elements_do_not_exist(browser):
    assert not browser.elements(id='non-existing')[0].exists


# eql
def test_returns_true_if_the_two_collections_have_the_same_elements(browser):
    a = browser.select_list(name='new_user_languages').options()
    b = browser.select_list(id='new_user_languages').options()

    assert a == b
    assert a.eql(b)


def test_returns_false_if_the_two_collections_are_not_the_same(browser):
    a = browser.select_list(name='new_user_languages').options()
    b = browser.select_list(id='new_user_role').options()

    assert a != b
    assert not a.eql(b)


@pytest.mark.page('non_control_elements.html')
def test_finds_elements_by_visible_text(browser):
    assert len(browser.links(visible_text='all visible')) == 1
    assert len(browser.links(visible_text=compile(r'all visible'))) == 1
    assert len(browser.links(visible_text='some visible')) == 1
    assert len(browser.links(visible_text=compile(r'some visible'))) == 1
    assert len(browser.links(visible_text='none visible')) == 0
    assert len(browser.links(visible_text=compile(r'none visible'))) == 0
