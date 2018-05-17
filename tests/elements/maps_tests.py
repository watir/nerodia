import pytest

pytestmark = pytest.mark.page('images.html')


class TestMaps(object):
    def test_with_selectors_returns_the_matching_elements(self, browser):
        assert list(browser.maps(name='triangle_map')) == [browser.map(name='triangle_map')]

    def test_returns_the_correct_number_of_maps(self, browser):
        assert len(browser.maps()) == 2

    def test_get_item_returns_the_map_at_the_given_index(self, browser):
        assert browser.maps()[0].id == 'triangle_map'

    def test_iterates_through_maps_correctly(self, browser):
        count = 0

        for index, map in enumerate(browser.maps()):
            assert map.name == browser.map(index=index).name
            assert map.id == browser.map(index=index).id
            count += 1

        assert count > 0
