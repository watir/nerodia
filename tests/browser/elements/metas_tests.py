import pytest

pytestmark = pytest.mark.page('forms_with_input_elements.html')


class TestMetas(object):
    def test_with_selectors_returns_the_matching_elements(self, browser):
        assert list(browser.metas(name='description')) == [browser.meta(name='description')]

    def test_returns_the_correct_number_of_metas(self, browser):
        assert len(browser.metas()) == 2

    def test_get_item_returns_the_meta_at_the_given_index(self, browser):
        assert browser.metas()[1].name == 'description'

    def test_iterates_through_metas_correctly(self, browser):
        count = 0

        for index, meta in enumerate(browser.metas()):
            assert meta.content == browser.meta(index=index).content
            count += 1

        assert count > 0
