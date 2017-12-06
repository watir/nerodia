import pytest

pytestmark = pytest.mark.page('images.html')


class TestImages(object):
    def test_with_selectors_returns_the_matching_elements(self, browser):
        assert browser.images(alt='circle').to_list == [browser.image(alt='circle')]

    def test_returns_the_correct_number_of_images(self, browser):
        assert len(browser.images()) == 10

    def test_get_item_returns_the_image_at_the_given_index(self, browser):
        assert browser.images()[5].id == 'square'

    def test_iterates_through_images_correctly(self, browser):
        count = 0

        for index, image in enumerate(browser.images()):
            assert image.id == browser.image(index=index).id
            count += 1

        assert count > 0
