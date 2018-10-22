import pytest

from nerodia.exception import UnknownObjectException

pytestmark = pytest.mark.page('definition_lists.html')


class TestDlExist(object):
    def test_returns_true_if_the_element_exists(self, browser):
        assert browser.dl(id='experience-list').exists
        assert browser.dl(class_name='list').exists
        assert browser.dl(xpath="//dl[@id='experience-list']").exists
        assert browser.dl(index=0).exists

    def test_returns_the_first_dl_if_given_no_args(self, browser):
        assert browser.dl().exists

    def test_returns_false_if_the_element_doesnt_exist(self, browser):
        assert not browser.dl(id='no_such_id').exists

    def test_raises_correct_exception_when_what_argument_is_invalid(self, browser):
        with pytest.raises(TypeError):
            browser.dl(id=3.14).exists


class TestDlAttributes(object):
    # id

    def test_returns_the_id_attribute_if_element_exists(self, browser):
        assert browser.dl(class_name='list').id == 'experience-list'

    def test_returns_an_empty_string_if_element_exists_but_id_doesnt(self, browser):
        assert browser.dl(class_name='personalia').id == ''

    @pytest.mark.parametrize('selector',
                             [{'id': 'no_such_id'},
                              {'title': 'no_such_title'},
                              {'index': 1337}])
    @pytest.mark.usefixtures('quick_timeout')
    def test_raises_correct_exception_for_id_if_element_does_not_exist(self, browser, selector):
        with pytest.raises(UnknownObjectException):
            browser.dl(**selector).id

    # title

    def test_returns_the_title_attribute_if_the_element_exists(self, browser):
        assert browser.dl(class_name='list').title == 'experience'

    # text

    def test_returns_the_text_of_the_element(self, browser):
        assert '11 years' in browser.dl(id='experience-list').text

    def test_returns_an_empty_string_if_element_exists_but_contains_no_text(self, browser):
        assert browser.dl(id='noop').text == ''

    @pytest.mark.parametrize('selector',
                             [{'id': 'no_such_id'},
                              {'title': 'no_such_title'},
                              {'index': 1337},
                              {'xpath': "//dl[@id='no_such_id']"}])
    @pytest.mark.usefixtures('quick_timeout')
    def test_raises_correct_exception_for_text_if_element_does_not_exist(self, browser, selector):
        with pytest.raises(UnknownObjectException):
            browser.delete(**selector).text


def test_finds_all_attribute_methods(browser):
    assert hasattr(browser.dl(index=0), 'id')
    assert hasattr(browser.dl(index=0), 'class_name')
    assert hasattr(browser.dl(index=0), 'style')
    assert hasattr(browser.dl(index=0), 'text')
    assert hasattr(browser.dl(index=0), 'title')


class TestDlManipulation(object):
    # click

    def test_fires_events_when_clicked(self, browser):
        assert browser.dt(id='name').text != 'changed!'
        browser.dt(id='name').click()
        assert browser.dt(id='name').text == 'changed!'

    @pytest.mark.parametrize('selector',
                             [{'id': 'no_such_id'},
                              {'title': 'no_such_title'},
                              {'index': 1337},
                              {'xpath': "//dl[@id='no_such_id']"}])
    @pytest.mark.usefixtures('quick_timeout')
    def test_raises_correct_exception_when_clicking_a_dl_that_doesnt_exist(self, browser, selector):
        with pytest.raises(UnknownObjectException):
            browser.button(**selector).click()

    # html

    # TODO xfail IE
    def test_returns_the_html_of_the_element(self, browser):
        html = browser.dl(id='experience-list').html.lower()
        assert '<dt class="current-industry">' in html
        assert '</body>' not in html

    # to_dict

    def test_converts_the_dl_to_a_dict(self, browser):
        expected = {
            'Experience': '11 years',
            'Education': 'Master',
            'Current industry': 'Architecture',
            'Previous industry experience': 'Architecture'
        }
        assert browser.dl(id='experience-list').to_dict() == expected
