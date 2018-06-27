import re

import pytest

pytestmark = pytest.mark.page('forms_with_input_elements.html')


class TestForms(object):
    def test_with_selectors_returns_the_matching_elements(self, browser):
        assert list(browser.forms(method='post')) == [browser.form(method='post')]

    def test_returns_the_correct_number_of_forms(self, browser):
        assert len(browser.forms()) == 2

    def test_get_item_returns_the_form_at_the_given_index(self, browser):
        assert re.search(r'post_to_me$', browser.forms()[0].action)  # varies between browsers
        assert browser.forms()[0].attribute_value('method') == 'post'

    def test_iterates_through_forms_correctly(self, browser):
        count = 0

        for index, form in enumerate(browser.forms()):
            assert form.name == browser.form(index=index).name
            assert form.id == browser.form(index=index).id
            assert form.class_name == browser.form(index=index).class_name
            count += 1

        assert count > 0
