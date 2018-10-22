import re

import pytest

pytestmark = pytest.mark.page('tables.html')


class TestTableExists(object):
    def test_returns_true_if_the_table_exists(self, browser):
        assert browser.table(id='axis_example').exists is True
        assert browser.table(id=re.compile('axis_example')).exists is True
        assert browser.table(index=0).exists is True
        assert browser.table(xpath="//table[@id='axis_example']").exists is True

    def test_returns_the_first_table_if_given_no_args(self, browser):
        assert browser.table().exists

    def test_returns_false_if_the_table_doesnt_exist(self, browser):
        assert not browser.table(id='no_such_id').exists
        assert not browser.table(id=re.compile('no_such_id')).exists
        assert not browser.table(index=1337).exists
        assert not browser.table(xpath="//table[@id='no_such_id']").exists

    def test_checks_the_tag_name_when_locating_by_xpath(self, browser):
        assert browser.table(xpath='//table//td').exists is False
        assert browser.table(xpath='//table').exists is True

    def test_raises_correct_exception_when_what_argument_is_invalid(self, browser):
        with pytest.raises(TypeError):
            browser.table(id=3.14).exists


class TestTableOther(object):
    def test_returns_a_two_dimensional_array_string_representation_of_the_table(self, browser):
        assert browser.table(id='inner').strings == [['Table 2, Row 1, Cell 1',
                                                      'Table 2, Row 1, Cell 2']]
        assert browser.table(id='outer').strings == [['Table 1, Row 1, Cell 1',
                                                      'Table 1, Row 1, Cell 2'],
                                                     ['Table 1, Row 2, Cell 1',
                                                      'Table 1, Row 2, Cell 2\nTable 2, Row 1, '
                                                      'Cell 1 Table 2, Row 1, Cell 2'],
                                                     ['Table 1, Row 3, Cell 1',
                                                      'Table 1, Row 3, Cell 2']]

    def test_returns_array_of_dicts_for_the_common_table_usage(self, browser):
        dict_table = [
            {'': 'March 2008', 'Before income tax': '', 'Income tax': '', 'After income tax': ''},
            {'': 'Gregory House', 'Before income tax': '5 934', 'Income tax': '1 347', 'After income tax': '4 587'},
            {'': 'Hugh Laurie', 'Before income tax': '6 300', 'Income tax': '1 479', 'After income tax': '4 821'},
            {'': 'April 2008', 'Before income tax': '', 'Income tax': '', 'After income tax': ''},
            {'': 'Gregory House', 'Before income tax': '5 863', 'Income tax': '1 331', 'After income tax': '4 532'},
            {'': 'Hugh Laurie', 'Before income tax': '6 252', 'Income tax': '1 420', 'After income tax': '4 832'},
            {'': 'Sum', 'Before income tax': '24 349', 'Income tax': '5 577', 'After income tax': '18 722'}
        ]
        assert browser.table(id='axis_example').dicts == dict_table

    @pytest.mark.page('uneven_table.html')
    def test_raises_correct_exception_if_table_could_not_be_parsed(self, browser):
        from nerodia.exception import Error
        with pytest.raises(Error) as e:
            browser.table().dicts
        assert e.value.args[0] == "row at index 0 has 2 cells, while header row has 3"

    def test_click_fires_the_tables_onclick_event(self, browser, messages):
        browser.table(id='inner').click()
        assert 'table' in messages.list

    def test_get_item_returns_the_nth_child_row(self, browser):
        assert browser.table(id='outer')[0].id == 'outer_first'
        assert browser.table(id='inner')[0].id == 'inner_first'
        assert browser.table(id='outer')[2].id == 'outer_last'


class TestTableRow(object):
    def test_finds_rows_belonging_to_this_table(self, browser):
        table = browser.table(id='outer')
        assert table.row(id='outer_last').exists
        assert table.row(text=re.compile('Table 1, Row 1, Cell 1')).exists

    def test_does_not_find_rows_from_a_nested_table(self, browser):
        table = browser.table(id='outer')
        assert table.row(id='inner_first').exists is False
        assert table.row(text=re.compile('\ATable 2, Row 1, Cell 1 '
                                         'Table 2, Row 1, Cell 2')).exists is False


class TestTableRows(object):
    def test_finds_the_correct_number_of_rows_excluding_nested_tables(self, browser):
        assert len(browser.table(id='inner').rows()) == 1
        assert len(browser.table(id='outer').rows()) == 3

    def test_finds_rows_matching_the_selector(self, browser):
        rows = browser.table(id='outer').rows(id=re.compile('first|last'))
        assert rows[0].id == 'outer_first'
        assert rows[-1].id == 'outer_last'

    def test_does_not_find_rows_from_a_nested_table(self, browser):
        assert len(browser.table(id='outer').rows(id='t2_r1_c1')) == 0


class TestTableBody(object):
    def test_returns_the_correct_instance_of_table_section(self, browser):
        from nerodia.elements.table_section import TableSection
        body = browser.table(index=0).tbody(id='first')
        assert isinstance(body, TableSection)
        assert body[0][0].text == 'March 2008'


class TestTableBodys(object):
    def test_returns_the_correct_instance_of_table_section_collection(self, browser):
        from nerodia.elements.html_elements import TableSectionCollection
        bodies = browser.table(index=0).tbodys()
        assert isinstance(bodies, TableSectionCollection)

        assert bodies[0].id == 'first'
        assert bodies[1].id == 'second'


class TestTableIter(object):
    def test_allows_iterating_over_the_rows_in_a_table(self, browser):
        from nerodia.elements.row import Row
        assert all(isinstance(x, Row) for x in browser.table(id='inner'))
