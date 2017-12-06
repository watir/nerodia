from re import compile

import pytest

pytestmark = pytest.mark.page('forms_with_input_elements.html')


class TestFormExist(object):
    def test_returns_true_if_the_form_exists(self, browser):
        assert browser.form(id='new_user').exists is True
        assert browser.form(id=compile(r'new_user')).exists is True
        assert browser.form(class_name='user').exists is True
        assert browser.form(class_name=compile(r'user')).exists is True
        assert browser.form(method='post').exists is True
        assert browser.form(method=compile(r'post')).exists is True
        assert browser.form(action=compile(r'to_me')).exists is True
        assert browser.form(index=0).exists is True
        assert browser.form(xpath="//form[@id='new_user']").exists is True

    def test_returns_the_first_form_if_given_no_args(self, browser):
        assert browser.form().exists

    def test_returns_false_if_the_form_does_not_exist(self, browser):
        assert browser.form(id='no_such_id').exists is False
        assert browser.form(id=compile(r'no_such_id')).exists is False
        assert browser.form(class_name='no_such_class').exists is False
        assert browser.form(class_name=compile(r'no_such_class')).exists is False
        assert browser.form(method='no_such_method').exists is False
        assert browser.form(method=compile(r'no_such_method')).exists is False
        assert browser.form(action='no_such_action').exists is False
        assert browser.form(action=compile(r'no_such_action')).exists is False
        assert browser.form(index=1337).exists is False
        assert browser.form(xpath="//form[@id='no_such_id']").exists is False

    def test_raises_correct_exception_when_what_argument_is_invalid(self, browser):
        with pytest.raises(TypeError):
            browser.form(id=3.14).exists

    def test_raises_correct_exception_when_how_argument_is_invalid(self, browser):
        from nerodia.exception import MissingWayOfFindingObjectException
        with pytest.raises(MissingWayOfFindingObjectException):
            browser.form(no_such_how='some_value').exists


class TestFormSubmit(object):
    def test_submits_the_form(self, browser):
        from nerodia.wait.wait import Wait
        browser.form(id='delete_user').submit()
        Wait.until(lambda: 'forms_with_input_elements.html' not in browser.url)
        assert 'Semantic table' in browser.text

    def test_triggers_onsbumit_event_and_takes_its_result_into_account(self, browser, messages):
        form = browser.form(name='user_new')
        form.submit()

        assert form.exists
        assert len(messages) == 1
        assert messages.list[0] == 'submit'
