import re

import pytest

pytestmark = pytest.mark.page('tables.html')


class TestTdExists(object):
    def test_returns_true_if_the_td_exists(self, browser):
        assert browser.td(id='t1_r2_c1').exists is True
        assert browser.td(id=re.compile('t1_r2_c1')).exists is True
        assert browser.td(text='Table 1, Row 3, Cell 1').exists is True
        assert browser.td(text=re.compile('Table 1')).exists is True
        assert browser.td(index=0).exists is True
        assert browser.td(xpath="//td[@id='t1_r2_c1']").exists is True

    def test_returns_the_first_td_if_given_no_args(self, browser):
        assert browser.td().exists

    def test_returns_false_if_the_td_doesnt_exist(self, browser):
        assert browser.td(id='no_such_id').exists is False
        assert browser.td(id=re.compile('no_such_id')).exists is False
        assert browser.td(text='no_such_text').exists is False
        assert browser.td(text=re.compile('no_such_text')).exists is False
        assert browser.td(index=1337).exists is False
        assert browser.td(xpath="//td[@id='no_such_id']").exists is False

    def test_raises_correct_exception_when_what_argument_is_invalid(self, browser):
        with pytest.raises(TypeError):
            browser.td(id=3.14).exists

    def test_raises_correct_exception_when_how_argument_is_invalid(self, browser):
        from nerodia.exception import MissingWayOfFindingObjectException
        with pytest.raises(MissingWayOfFindingObjectException):
            browser.td(no_such_how='some_value').exists


class TestTdClick(object):
    def test_fires_the_tables_onclick_event(self, browser, messages):
        browser.td(id='t2_r1_c1').click()
        assert 'td' in messages.list


class TestTdAttributes(object):
    def test_returns_the_text_inside_the_td(self, browser):
        assert browser.td(id='t1_r2_c1').text == 'Table 1, Row 2, Cell 1'
        assert browser.td(id='t2_r1_c1').text == 'Table 2, Row 1, Cell 1'

    def test_gets_the_colspan_attribute(self, browser):
        assert browser.td(id='colspan_2').colspan == 2
        assert browser.td(id='no_colspan').colspan == 1


def test_finds_all_attribute_methods(browser):
    assert hasattr(browser.td(index=0), 'text')
    assert hasattr(browser.td(index=0), 'colspan')


class TestTdOther(object):
    def test_returns_the_corresponding_column_header(self, browser):
        header = browser.td(text='1 331').column_header
        assert header == 'Income tax'

    def test_returns_the_corresponding_sibling_cell_by_text(self, browser):
        local_td = browser.td(text='1 331')
        td = local_td.sibling_from_header(text='After income tax')

        assert td.text == '4 532'

    def test_returns_the_corresponding_sibling_cell_by_index(self, browser):
        local_td = browser.td(text='1 331')
        td = local_td.sibling_from_header(text=re.compile('tax'), index=2)

        assert td.text == '4 532'
