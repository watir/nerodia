from re import compile

import pytest

pytestmark = pytest.mark.page('tables.html')


class TestTableHeaderExist(object):
    def test_returns_true_if_the_element_exists(self, browser):
        assert browser.thead(id='tax_headers').exists is True
        assert browser.thead(id=compile(r'tax_headers')).exists is True
        assert browser.thead(index=0).exists is True
        assert browser.thead(xpath="//thead[@id='tax_headers']").exists is True

    def test_returns_true_if_the_element_exists_within_table(self, browser):
        assert browser.table(index=0).thead(id='tax_headers').exists is True
        assert browser.table(index=0).thead(id=compile(r'tax_headers')).exists is True
        assert browser.table(index=0).thead(index=0).exists is True
        assert browser.table(index=0).thead(xpath="//thead[@id='tax_headers']").exists is True

    def test_returns_the_first_thead_if_given_no_args(self, browser):
        assert browser.thead().exists

    def test_returns_false_if_the_element_does_not_exist(self, browser):
        assert browser.thead(id='no_such_id').exists is False
        assert browser.thead(id=compile(r'no_such_id')).exists is False
        assert browser.thead(index=1337).exists is False
        assert browser.thead(xpath="//thead[@id='no_such_id']").exists is False

    def test_returns_false_if_the_element_does_not_exist_within_table(self, browser):
        assert browser.table(index=0).thead(id='no_such_id').exists is False
        assert browser.table(index=0).thead(id=compile(r'no_such_id')).exists is False
        assert browser.table(index=0).thead(index=1337).exists is False
        assert browser.table(index=0).thead(xpath="//thead[@id='no_such_id']").exists is False

    def test_raises_correct_exception_when_what_argument_is_invalid(self, browser):
        with pytest.raises(TypeError):
            browser.thead(id=3.14).exists


class TestTableHeaderOther(object):
    # get_item

    def test_returns_the_row_at_the_given_index(self, browser):
        assert browser.thead(id='tax_headers')[0].id == 'thead_row_1'
        assert browser.thead(id='tax_headers')[0][1].text == 'Before income tax'
        assert browser.thead(id='tax_headers')[0][2].text == 'Income tax'

    def test_returns_the_row_at_the_given_index_within_table(self, browser):
        assert browser.table(index=0).thead(id='tax_headers')[0].id == 'thead_row_1'
        assert browser.table(index=0).thead(id='tax_headers')[0][1].text == 'Before income tax'
        assert browser.table(index=0).thead(id='tax_headers')[0][2].text == 'Income tax'

    # row

    def test_finds_the_first_row_matching_the_selector(self, browser):
        assert browser.thead(id='tax_headers').row(class_name='dark').id == 'thead_row_1'

    # rows

    def test_finds_rows_matching_the_selector(self, browser):
        rows = browser.thead(id='tax_headers').rows(class_name='dark')

        assert len(rows) == 1
        assert rows[0].id == 'thead_row_1'

    # strings

    def test_returns_the_text_of_child_cells(self, browser):
        assert browser.thead(id='tax_headers').strings == [['', 'Before income tax', 'Income tax', 'After income tax']]
