import pytest

pytestmark = pytest.mark.page('non_control_elements.html')


def test_returns_the_matching_elements(browser):
    assert browser.deletes(class_name='lead').to_list == [browser.delete(class_name='lead')]


def test_returns_the_number_of_deletes(browser):
    assert len(browser.deletes()) == 5


def test_returns_the_delete_at_the_given_index(browser):
    assert browser.deletes()[0].id == 'lead'


def test_iterates_through_deletes_correctly(browser):
    count = 0
    for index, d in enumerate(browser.deletes()):
        assert d.id == browser.delete(index=index).id
        count += 1
    assert count > 0
