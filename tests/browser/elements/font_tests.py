import pytest

pytestmark = pytest.mark.page('font.html')


class TestFont(object):
    def test_finds_the_font_element(self, browser):
        assert browser.font(index=0).exists

    def test_knows_about_the_color_attribute(self, browser):
        assert browser.font(index=0).color == '#ff00ff'

    def test_knows_about_the_face_attribute(self, browser):
        assert browser.font(index=0).face == 'Helvetica'

    def test_knows_about_the_size_attribute(self, browser):
        assert browser.font(index=0).size == '12'

    def test_finds_all_font_elements(self, browser):
        assert len(browser.fonts()) == 1
