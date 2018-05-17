import pytest


@pytest.fixture
def reset_form(browser_manager):
    yield
    browser_manager.instance.link().click()


pytestmark = [pytest.mark.page('forms_with_input_elements.html'),
              pytest.mark.usefixtures('reset_form')]


class TestSelectLists(object):
    def test_with_selectors_returns_the_matching_elements(self, browser):
        assert list(browser.select_lists(name='delete_user_username')) == \
            [browser.select_list(name='delete_user_username')]

    def test_returns_the_correct_number_of_select_lists_on_the_page(self, browser):
        assert len(browser.select_lists()) == 6

    def test_get_item_returns_the_correct_item(self, browser):
        assert browser.select_lists()[0].value == '2'
        assert browser.select_lists()[0].name == 'new_user_country'
        assert browser.select_lists()[0].multiple is False
        assert browser.select_lists()[1].multiple is True

    def test_iterates_through_the_select_lists_correctly(self, browser):
        count = 0
        for index, list in enumerate(browser.select_lists()):
            assert browser.select_list(index=index).name == list.name
            assert browser.select_list(index=index).id == list.id
            assert browser.select_list(index=index).value == list.value
            count += 1
        assert count > 0
