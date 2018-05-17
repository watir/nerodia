import pytest

pytestmark = pytest.mark.page('frames.html')


class TestFrames(object):
    def test_with_selectors_returns_the_matching_elements(self, browser):
        assert list(browser.frames(name='frame2')) == [browser.frame(name='frame2')]

    def test_returns_the_correct_number_of_frames(self, browser):
        assert len(browser.frames()) == 2

    def test_get_item_returns_the_frame_at_the_given_index(self, browser):
        assert browser.frames()[0].id == 'frame_1'

    def test_iterates_through_frames_correctly(self, browser):
        count = 0

        for index, frame in enumerate(browser.frames()):
            assert frame.name == browser.frame(index=index).name
            assert frame.id == browser.frame(index=index).id
            count += 1

        assert count > 0
