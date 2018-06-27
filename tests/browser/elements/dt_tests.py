import pytest

from nerodia.exception import UnknownObjectException

pytestmark = pytest.mark.page('definition_lists.html')


class TestDtExist(object):
    def test_returns_true_if_the_element_exists(self, browser):
        assert browser.dt(id='experience').exists
        assert browser.dt(class_name='current-industry').exists
        assert browser.dt(xpath="//dt[@id='experience']").exists
        assert browser.dt(index=0).exists

    def test_returns_the_first_dt_if_given_no_args(self, browser):
        assert browser.dt().exists

    def test_returns_false_if_the_element_doesnt_exist(self, browser):
        assert not browser.dt(id='no_such_id').exists

    def test_raises_correct_exception_when_what_argument_is_invalid(self, browser):
        with pytest.raises(TypeError):
            browser.dt(id=3.14).exists


class TestDtAttributes(object):
    # class_name

    def test_returns_the_class_name_if_element_exists(self, browser):
        assert browser.dt(id='experience').class_name == 'industry'

    def test_returns_an_empty_string_if_element_exists_but_class_name_doesnt(self, browser):
        assert browser.dt(id='education').class_name == ''

    @pytest.mark.parametrize('selector',
                             [{'id': 'no_such_id'},
                              {'title': 'no_such_title'},
                              {'index': 1337},
                              {'xpath': "//dt[@id='no_such_id']"}])
    @pytest.mark.usefixtures('quick_timeout')
    def test_raises_correct_exception_for_class_name_if_element_does_not_exist(self, browser, selector):
        with pytest.raises(UnknownObjectException):
            browser.dt(**selector).class_name

    # id

    def test_returns_the_id_attribute_if_element_exists(self, browser):
        assert browser.dt(class_name='industry').id == 'experience'

    def test_returns_an_empty_string_if_element_exists_but_id_doesnt(self, browser):
        assert browser.dt(class_name='current-industry').id == ''

    @pytest.mark.parametrize('selector',
                             [{'id': 'no_such_id'},
                              {'title': 'no_such_title'},
                              {'index': 1337}])
    @pytest.mark.usefixtures('quick_timeout')
    def test_raises_correct_exception_for_id_if_element_does_not_exist(self, browser, selector):
        with pytest.raises(UnknownObjectException):
            browser.dt(**selector).id

    # title

    def test_returns_the_title_attribute_if_the_element_exists(self, browser):
        assert browser.dt(id='experience').title == 'experience'

    # text

    def test_returns_the_text_of_the_element(self, browser):
        assert browser.dt(id='experience').text == 'Experience'

    def test_returns_an_empty_string_if_element_exists_but_contains_no_text(self, browser):
        assert browser.dt(class_name='noop').text == ''

    @pytest.mark.parametrize('selector',
                             [{'id': 'no_such_id'},
                              {'title': 'no_such_title'},
                              {'index': 1337},
                              {'xpath': "//dt[@id='no_such_id']"}])
    @pytest.mark.usefixtures('quick_timeout')
    def test_raises_correct_exception_for_text_if_element_does_not_exist(self, browser, selector):
        with pytest.raises(UnknownObjectException):
            browser.delete(**selector).text


def test_finds_all_attribute_methods(browser):
    assert hasattr(browser.dt(index=0), 'id')
    assert hasattr(browser.dt(index=0), 'class_name')
    assert hasattr(browser.dt(index=0), 'style')
    assert hasattr(browser.dt(index=0), 'text')
    assert hasattr(browser.dt(index=0), 'title')


class TestDtManipulation(object):
    # click

    def test_fires_events_when_clicked(self, browser):
        assert browser.dt(id='education').text != 'changed'
        browser.dt(id='education').click()
        assert browser.dt(id='education').text == 'changed'

    @pytest.mark.parametrize('selector',
                             [{'id': 'no_such_id'},
                              {'title': 'no_such_title'},
                              {'index': 1337},
                              {'xpath': "//dt[@id='no_such_id']"}])
    @pytest.mark.usefixtures('quick_timeout')
    def test_raises_correct_exception_when_clicking_a_dt_that_doesnt_exist(self, browser, selector):
        with pytest.raises(UnknownObjectException):
            browser.button(**selector).click()

    # html

    # TODO xfail IE
    def test_returns_the_html_of_the_element(self, browser):
        from re import search
        html = browser.dt(id='name').html.lower()
        assert search(r'<div>.*name.*</div>', html)
        assert '</body>' not in html
