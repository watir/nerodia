import pytest

pytestmark = pytest.mark.page('non_control_elements.html')


class TestHns(object):
    def test_with_selectors_returns_the_matching_elements(self, browser):
        assert list(browser.h1s(class_name='primary')) == [browser.h1(class_name='primary')]

    def test_returns_the_correct_number_of_hns(self, browser):
        assert len(browser.h2s()) == 9

    def test_get_item_returns_the_hn_at_the_given_index(self, browser):
        assert browser.h1s()[0].id == 'first_header'

    def test_iterates_through_hns_correctly(self, browser):
        lengths = []
        for h in range(1, 7):
            collection = getattr(browser, 'h{}s'.format(h))()
            for index, header in enumerate(collection):
                assert getattr(browser, 'h{}'.format(h))(index=index).id == header.id
            lengths.append(len(collection))

        assert lengths == [2, 9, 2, 1, 1, 2]
