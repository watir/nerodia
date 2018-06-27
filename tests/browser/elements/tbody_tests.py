from re import compile

import pytest

pytestmark = pytest.mark.page('tables.html')


class TestTbodyExist(object):
    def test_returns_true_if_the_element_exists(self, browser):
        assert browser.tbody(id='first').exists is True
        assert browser.tbody(id=compile(r'first')).exists is True
        assert browser.tbody(index=0).exists is True
        assert browser.tbody(xpath="//tbody[@id='first']").exists is True

    def test_returns_true_if_the_element_exists_in_table(self, browser):
        assert browser.table(index=0).tbody(id='first').exists is True
        assert browser.table(index=0).tbody(id=compile(r'first')).exists is True
        assert browser.table(index=0).tbody(index=0).exists is True
        assert browser.table(index=0).tbody(xpath="//tbody[@id='first']").exists is True

    def test_returns_the_first_tbody_if_given_no_args(self, browser):
        assert browser.tbody().exists

    def test_returns_false_if_the_element_does_not_exist(self, browser):
        assert browser.tbody(id='no_such_id').exists is False
        assert browser.tbody(id=compile(r'no_such_id')).exists is False
        assert browser.tbody(index=1337).exists is False
        assert browser.tbody(xpath="//tbody[@id='no_such_id']").exists is False

    def test_returns_false_if_the_element_does_not_exist_in_table(self, browser):
        assert browser.table(index=0).tbody(id='no_such_id').exists is False
        assert browser.table(index=0).tbody(id=compile(r'no_such_id')).exists is False
        assert browser.table(index=0).tbody(index=1337).exists is False
        assert browser.table(index=0).tbody(xpath="//tbody[@id='no_such_id']").exists is False

    def test_raises_correct_exception_when_what_argument_is_invalid(self, browser):
        with pytest.raises(TypeError):
            browser.tbody(id=3.14).exists


class TestTbodyOther(object):
    def test_finds_the_first_row_matching_the_selector(self, browser):
        row = browser.tbody(id='first').row(id='gregory')
        assert row.tag_name == 'tr'
        assert row.id == 'gregory'

    def test_finds_rows_matching_the_selector(self, browser):
        rows = browser.tbody(id='first').rows(id=compile(r'h$'))

        assert len(rows) == 2
        assert rows[0].id == 'march'
        assert rows[-1].id == 'hugh'

    def test_returns_the_text_of_child_cells(self, browser):
        assert browser.tbody(id='first').strings == [['March 2008', '', '', ''],
                                                     ['Gregory House', '5 934', '1 347', '4 587'],
                                                     ['Hugh Laurie', '6 300', '1 479', '4 821']]
