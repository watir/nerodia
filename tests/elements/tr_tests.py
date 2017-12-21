import re

import pytest

pytestmark = pytest.mark.page('tables.html')


class TestTrExists(object):
    def test_returns_true_if_the_tr_exists(self, browser):
        assert browser.tr(id='outer_first').exists is True
        assert browser.tr(id=re.compile('outer_first')).exists is True
        assert browser.tr(index=0).exists is True
        assert browser.tr(xpath="//tr[@id='outer_first']").exists is True

    def test_returns_the_first_tr_if_given_no_args(self, browser):
        assert browser.tr().exists

    def test_returns_false_if_the_tr_doesnt_exist(self, browser):
        assert browser.tr(id='no_such_id').exists is False
        assert browser.tr(id=re.compile('no_such_id')).exists is False
        assert browser.tr(index=1337).exists is False
        assert browser.tr(xpath="//tr[@id='no_such_id']").exists is False

    def test_raises_correct_exception_when_what_argument_is_invalid(self, browser):
        with pytest.raises(TypeError):
            browser.tr(id=3.14).exists


class TestTrClick(object):
    @pytest.mark.only('safari')
    def test_fires_the_tables_onclick_event(self, browser, messages):
        browser.tr(id='inner_first').click()
        assert 'tr' in messages.list


class TestTrOther(object):
    def test_returns_the_correct_number_of_cells(self, browser):
        table = browser.table(id='outer')
        assert len(table[0].cells()) == 2
        assert len(table[1].cells()) == 2
        assert len(table[2].cells()) == 2

    def test_finds_cells_in_the_table(self, browser):
        assert len(browser.table(id='outer')[0].cells(text=re.compile('Table 1'))) == 2

    def test_does_not_find_cells_from_nested_tables(self, browser):
        table = browser.table(id='outer')
        assert table[1].cell(id='t2_r1_c1').exists is False
        assert table[1].cell(id=re.compile('t2_r1_c1')).exists is False

    def test_iterates_correctly_through_the_cells_of_the_row(self, browser):
        for index, cell in enumerate(browser.table(id='outer').row(index=1).cells()):
            assert cell.id == 't1_r2_c{}'.format(index + 1)
