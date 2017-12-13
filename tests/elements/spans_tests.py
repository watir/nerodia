import pytest

pytestmark = pytest.mark.page('non_control_elements.html')


class TestSpans(object):
    def test_with_selectors_returns_the_matching_elements(self, browser):
        assert browser.spans(class_name='footer').to_list == [browser.span(class_name='footer')]

    def test_returns_the_correct_number_of_spans(self, browser):
        assert len(browser.spans()) == 6

    def test_get_item_returns_the_span_at_the_given_index(self, browser):
        assert browser.spans()[0].id == 'lead'

    def test_iterates_through_spans_correctly(self, browser):
        count = 0

        for index, span in enumerate(browser.spans()):
            assert span.id == browser.span(index=index).id
            count += 1

        assert count > 0
