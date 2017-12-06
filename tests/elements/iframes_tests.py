import pytest

pytestmark = pytest.mark.page('iframes.html')


class TestIFrames(object):
    def test_with_selectors_returns_the_matching_elements(self, browser):
        assert browser.iframes(id='iframe_2').to_list == [browser.iframe(id='iframe_2')]

    def test_matches_equality_of_iframe_with_that_from_a_collection(self, browser):
        assert browser.iframes()[-1] == browser.iframe(id='iframe_2')

    def test_returns_the_correct_number_of_iframes(self, browser):
        assert len(browser.iframes()) == 2

    def test_get_item_returns_the_frame_at_the_given_index(self, browser):
        assert browser.iframes()[0].id == 'iframe_1'

    def test_iterates_through_iframes_correctly(self, browser):
        count = 0

        for index, iframe in enumerate(browser.iframes()):
            assert iframe.name == browser.iframe(index=index).name
            assert iframe.id == browser.iframe(index=index).id
            count += 1

        assert count > 0
