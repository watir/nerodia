from re import compile

import pytest

pytestmark = pytest.mark.page('tables.html')


class TestTableFooterExist(object):
    def test_returns_true_if_the_element_exists(self, browser):
        assert browser.tfoot(id='tax_totals').exists is True
        assert browser.tfoot(id=compile(r'tax_totals')).exists is True
        assert browser.tfoot(index=0).exists is True
        assert browser.tfoot(xpath="//tfoot[@id='tax_totals']").exists is True

    def test_returns_true_if_the_element_exists_within_table(self, browser):
        assert browser.table(index=0).tfoot(id='tax_totals').exists is True
        assert browser.table(index=0).tfoot(id=compile(r'tax_totals')).exists is True
        assert browser.table(index=0).tfoot(index=0).exists is True
        assert browser.table(index=0).tfoot(xpath="//tfoot[@id='tax_totals']").exists is True

    def test_returns_the_first_tfoot_if_given_no_args(self, browser):
        assert browser.tfoot().exists

    def test_returns_false_if_the_element_does_not_exist(self, browser):
        assert browser.tfoot(id='no_such_id').exists is False
        assert browser.tfoot(id=compile(r'no_such_id')).exists is False
        assert browser.tfoot(index=1337).exists is False
        assert browser.tfoot(xpath="//tfoot[@id='no_such_id']").exists is False

    def test_returns_false_if_the_element_does_not_exist_within_table(self, browser):
        assert browser.table(index=0).tfoot(id='no_such_id').exists is False
        assert browser.table(index=0).tfoot(id=compile(r'no_such_id')).exists is False
        assert browser.table(index=0).tfoot(index=1337).exists is False
        assert browser.table(index=0).tfoot(xpath="//tfoot[@id='no_such_id']").exists is False

    def test_raises_correct_exception_when_what_argument_is_invalid(self, browser):
        with pytest.raises(TypeError):
            browser.tfoot(id=3.14).exists

    def test_raises_correct_exception_when_how_argument_is_invalid(self, browser):
        from nerodia.exception import MissingWayOfFindingObjectException
        with pytest.raises(MissingWayOfFindingObjectException):
            browser.tfoot(no_such_how='some_value').exists


class TestTableFooterOther(object):
    # get_item

    def test_returns_the_row_at_the_given_index(self, browser):
        assert browser.tfoot(id='tax_totals')[0].id == 'tfoot_row_1'
        assert browser.tfoot(id='tax_totals')[0][1].text == '24 349'
        assert browser.tfoot(id='tax_totals')[0][2].text == '5 577'

    def test_returns_the_row_at_the_given_index_within_table(self, browser):
        assert browser.table(index=0).tfoot(id='tax_totals')[0].id == 'tfoot_row_1'
        assert browser.table(index=0).tfoot(id='tax_totals')[0][1].text == '24 349'
        assert browser.table(index=0).tfoot(id='tax_totals')[0][2].text == '5 577'

    # row

    def test_finds_rows_matching_the_selector(self, browser):
        rows = browser.tfoot(id='tax_totals').rows(id='tfoot_row_1')

        assert len(rows) == 1
        assert rows[0].id == 'tfoot_row_1'

    # strings

    def test_returns_the_text_of_child_cells(self, browser):
        assert browser.tfoot(id='tax_totals').strings == [['Sum', '24 349', '5 577', '18 722']]
