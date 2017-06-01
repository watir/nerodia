import pytest

from nerodia.elements.html_elements import Div, Span, HTMLElement, HTMLElementCollection

pytestmark = pytest.mark.page('nested_elements.html')


class TestAdjacentParent(object):
    def test_gets_immediate_parent_of_an_element_by_default(self, browser):
        assert browser.div(id='first_sibling').parent().id == 'parent'
        assert isinstance(browser.div(id='first_sibling').parent(), HTMLElement)

    def test_accepts_index_argument(self, browser):
        assert browser.div(id='first_sibling').parent(index=2).id == 'grandparent'
        assert isinstance(browser.div(id='first_sibling').parent(index=2), HTMLElement)

    def test_accepts_tag_name_argument(self, browser):
        assert browser.div(id='first_sibling').parent(tag_name='div').id == 'parent'
        assert isinstance(browser.div(id='first_sibling').parent(tag_name='div'), Div)

    def test_accepts_index_and_tag_name_arguments(self, browser):
        assert browser.div(id="first_sibling").parent(tag_name='div', index=1).id == 'grandparent'
        assert isinstance(browser.div(id="first_sibling").parent(tag_name='div', index=1), Div)

    def test_does_not_error_when_no_parent_element_of_an_index_exists(self, browser):
        assert not browser.body().parent(index=2).exists

    def test_does_not_error_when_no_parent_element_of_a_tag_name_exists(self, browser):
        assert not browser.div(id='first_sibling').parent(tag_name='table').exists


class TestAdjacentFollowingSibling(object):
    def test_gets_immediate_following_sibling_of_an_element_by_default(self, browser):
        assert browser.div(id='first_sibling').following_sibling().id == 'between_siblings1'
        assert isinstance(browser.div(id='first_sibling').following_sibling(), HTMLElement)

    def test_accepts_index_argument(self, browser):
        assert browser.div(id='first_sibling').following_sibling(index=2).id == 'between_siblings2'
        assert isinstance(browser.div(id='first_sibling').following_sibling(index=2), HTMLElement)

    def test_accepts_tag_name_argument(self, browser):
        assert browser.div(id='first_sibling').following_sibling(
            tag_name='div').id == 'second_sibling'
        assert isinstance(browser.div(id='first_sibling').following_sibling(tag_name='div'), Div)

    def test_accepts_index_and_tag_name_arguments(self, browser):
        assert browser.div(id='first_sibling').following_sibling(tag_name='div',
                                                                 index=1).id == 'third_sibling'
        assert isinstance(
            browser.div(id='first_sibling').following_sibling(tag_name='div', index=1), Div)

    def test_does_not_error_when_no_next_sibling_of_an_index_exists(self, browser):
        assert not browser.body().following_sibling(index=1).exists

    def test_does_not_error_when_no_next_sibling_of_a_tag_name_exists(self, browser):
        assert not browser.div(id='first_sibling').following_sibling(tag_name='table').exists


class TestAdjacentFollowingSiblings(object):
    def test_gets_collection_of_subsequent_siblings_of_an_element_by_default(self, browser):
        assert isinstance(browser.div(id='second_sibling').following_siblings(),
                          HTMLElementCollection)
        assert len(browser.div(id='second_sibling').following_siblings()) == 2

    def test_accepts_tag_name_argument(self, browser):
        assert len(browser.div(id='second_sibling').following_siblings(tag_name='div')) == 1
        assert isinstance(browser.div(id='second_sibling').following_siblings(tag_name='div')[0],
                          Div)


class TestAdjacentPreviousSibling(object):
    def test_gets_immediate_preceeding_sibling_of_an_element_by_default(self, browser):
        assert browser.div(id='third_sibling').previous_sibling().id == 'between_siblings2'
        assert isinstance(browser.div(id='third_sibling').previous_sibling(), HTMLElement)

    def test_accepts_index_argument(self, browser):
        assert browser.div(id='third_sibling').previous_sibling(index=2).id == 'between_siblings1'
        assert isinstance(browser.div(id='third_sibling').previous_sibling(index=2), HTMLElement)

    def test_accepts_tag_name_argument(self, browser):
        assert browser.div(id='third_sibling').previous_sibling(
            tag_name='div').id == 'second_sibling'
        assert isinstance(browser.div(id='third_sibling').previous_sibling(tag_name='div'), Div)

    def test_accepts_index_and_tag_name_arguments(self, browser):
        assert browser.div(id='third_sibling').previous_sibling(tag_name='div',
                                                                index=1).id == 'first_sibling'
        assert isinstance(browser.div(id='third_sibling').previous_sibling(tag_name='div', index=1),
                          Div)

    def test_does_not_error_when_no_next_sibling_of_an_index_exists(self, browser):
        assert not browser.body().previous_sibling(index=1).exists

    def test_does_not_error_when_no_next_sibling_of_a_tag_name_exists(self, browser):
        assert not browser.div(id='third_sibling').previous_sibling(tag_name='table').exists


class TestAdjacentPreviousSiblings(object):
    def test_gets_collection_of_subsequent_siblings_of_an_element_by_default(self, browser):
        assert isinstance(browser.div(id='second_sibling').previous_siblings(),
                          HTMLElementCollection)
        assert len(browser.div(id='second_sibling').previous_siblings()) == 2

    def test_accepts_tag_name_argument(self, browser):
        assert len(browser.div(id='second_sibling').previous_siblings(tag_name='div')) == 1
        assert isinstance(browser.div(id='second_sibling').previous_siblings(tag_name='div')[0],
                          Div)


class TestAdjacentChild(object):
    def test_gets_immediate_child_of_an_element_by_default(self, browser):
        assert browser.div(id='parent').child().id == 'first_sibling'
        assert isinstance(browser.div(id='parent').child(), HTMLElement)

    def test_accepts_index_argument(self, browser):
        assert browser.div(id='parent').child(index=2).id == 'second_sibling'
        assert isinstance(browser.div(id='parent').child(index=2), HTMLElement)

    def test_accepts_tag_name_argument(self, browser):
        assert browser.div(id='parent').child(tag_name='span').id == 'between_siblings1'
        assert isinstance(browser.div(id='parent').child(tag_name='span'), Span)

    def test_accepts_index_and_tag_name_arguments(self, browser):
        assert browser.div(id='parent').child(tag_name='div', index=1).id == 'second_sibling'
        assert isinstance(browser.div(id='parent').child(tag_name='div', index=1), Div)

    def test_does_not_error_when_no_next_sibling_of_an_index_exists(self, browser):
        assert not browser.div(id='second_sibling').child(index=1).exists

    def test_does_not_error_when_no_next_sibling_of_a_tag_name_exists(self, browser):
        assert not browser.div(id='parent').child(tag_name='table').exists


class TestAdjacentChildren(object):
    def test_gets_collection_of_children_of_an_element_by_default(self, browser):
        assert isinstance(browser.div(id='parent').children(), HTMLElementCollection)
        assert len(browser.div(id='parent').children()) == 5

    def test_accepts_tag_name_argument(self, browser):
        children = browser.div(id='parent').children(tag_name='div')
        assert len(children) == 3
        assert all(isinstance(child, Div) for child in children)
