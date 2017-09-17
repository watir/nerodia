import pytest

pytestmark = pytest.mark.page('non_control_elements.html')


class TestEmExist(object):
    def test_returns_true_if_the_element_exists(self, browser):
        assert browser.em(id='important-id').exists
        assert browser.em(class_name='important-class').exists
        assert browser.em(xpath="//em[@id='important-id']").exists
        assert browser.em(index=0).exists

    def test_returns_the_first_em_if_given_no_args(self, browser):
        assert browser.em().exists

    def test_returns_false_if_the_element_doesnt_exist(self, browser):
        assert not browser.em(id='no_such_id').exists

    def test_raises_correct_exception_when_what_argument_is_invalid(self, browser):
        with pytest.raises(TypeError):
            browser.em(id=3.14).exists

    def test_raises_correct_exception_when_how_argument_is_invalid(self, browser):
        from nerodia.exception import MissingWayOfFindingObjectException
        with pytest.raises(MissingWayOfFindingObjectException):
            browser.em(no_such_how='some_value').exists


class TestEmAttributes(object):
    # class_name

    def test_returns_the_class_name_if_element_exists(self, browser):
        assert browser.em(id='important-id').class_name == 'important-class'

    @pytest.mark.parametrize('selector',
                             [{'id': 'no_such_id'},
                              {'title': 'no_such_title'},
                              {'index': 1337},
                              {'xpath': "//em[@id='no_such_id']"}])
    def test_raises_correct_exception_for_class_name_if_element_does_not_exist(self, browser, selector):
        from nerodia.exception import UnknownObjectException
        with pytest.raises(UnknownObjectException):
            browser.em(**selector).class_name

    # id

    def test_returns_the_id_attribute_if_element_exists(self, browser):
        assert browser.em(class_name='important-class').id == 'important-id'

    @pytest.mark.parametrize('selector',
                             [{'id': 'no_such_id'},
                              {'title': 'no_such_title'},
                              {'index': 1337}])
    def test_raises_correct_exception_for_id_if_element_does_not_exist(self, browser, selector):
        from nerodia.exception import UnknownObjectException
        with pytest.raises(UnknownObjectException):
            browser.em(**selector).id

    # title

    def test_returns_the_title_of_the_element(self, browser):
        assert browser.em(class_name='important-class').title == 'ergo cogito'

    # text

    def test_returns_the_text_of_the_element(self, browser):
        assert browser.em(id='important-id').text == 'ergo cogito'

    @pytest.mark.parametrize('selector',
                             [{'id': 'no_such_id'},
                              {'title': 'no_such_title'},
                              {'index': 1337}])
    def test_raises_correct_exception_for_text_if_element_does_not_exist(self, browser, selector):
        from nerodia.exception import UnknownObjectException
        with pytest.raises(UnknownObjectException):
            browser.em(**selector).text


def test_finds_all_attribute_methods(browser):
    assert hasattr(browser.em(index=0), 'id')
    assert hasattr(browser.em(index=0), 'class_name')
    assert hasattr(browser.em(index=0), 'style')
    assert hasattr(browser.em(index=0), 'text')
    assert hasattr(browser.em(index=0), 'title')


class TestEmManipulation(object):
    # click

    @pytest.mark.parametrize('selector',
                             [{'id': 'no_such_id'},
                              {'title': 'no_such_title'},
                              {'index': 1337},
                              {'xpath': "//em[@id='no_such_id']"}])
    def test_raises_correct_exception_when_clicking_an_em_that_doesnt_exist(self, browser, selector):
        from nerodia.exception import UnknownObjectException
        with pytest.raises(UnknownObjectException):
            browser.em(**selector).click()
