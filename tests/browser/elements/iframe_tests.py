from re import compile

import pytest

from nerodia.exception import UnknownFrameException, UnknownObjectException

pytestmark = pytest.mark.page('iframes.html')


@pytest.mark.xfail_firefox(reason='bug yet to be entered with the new webdriver click')
def test_handles_cross_iframe_javascript(browser):
    assert browser.iframe(id='iframe_1').text_field(name='senderElement').value == 'send_this_value'
    assert browser.iframe(id='iframe_2').text_field(name='recieverElement').value == 'old_value'
    browser.iframe(id='iframe_1').button(id='send').click()
    assert browser.iframe(id='iframe_2').text_field(name='recieverElement').value == 'send_this_value'


def test_locates_an_element_defined_by_selenium_element(browser):
    iframe = browser.iframe(id='iframe_1').locate()
    se_element = iframe.el
    iframe2 = browser.element(element=se_element).to_subtype()
    assert iframe2 == iframe


class TestIFrameWd(object):
    def test_returns_a_nerodia_framed_driver_instance(self, browser):
        from nerodia.elements.i_frame import FramedDriver
        iframe = browser.iframe(id='iframe_1')
        assert isinstance(iframe.wd, FramedDriver)

    def test_properly_delegates_driver_commands(self, browser):
        iframe = browser.iframe(id='iframe_1')
        assert iframe.wd.title == 'Iframes'

    def test_properly_delegates_element_commands(self, browser):
        iframe = browser.iframe(id='iframe_1')
        assert iframe.wd.get_attribute('id') == 'iframe_1'


class TestIFrameExist(object):
    def test_returns_true_if_the_iframe_exists(self, browser):
        assert browser.iframe(id='iframe_1').exists is True
        assert browser.iframe(id=compile(r'iframe')).exists is True
        assert browser.iframe(name='iframe1').exists is True
        assert browser.iframe(name=compile(r'iframe')).exists is True
        assert browser.iframe(class_name='half').exists is True
        assert browser.iframe(class_name=compile(r'half')).exists is True
        assert browser.iframe(src='iframe_1.html').exists is True
        assert browser.iframe(src=compile(r'iframe_1')).exists is True
        assert browser.iframe(index=0).exists is True
        assert browser.iframe(xpath="//iframe[@id='iframe_1']").exists is True

    def test_returns_the_first_iframe_if_given_no_args(self, browser):
        assert browser.iframe().exists

    def test_returns_false_if_the_iframe_does_not_exist(self, browser):
        assert browser.iframe(id='no_such_id').exists is False
        assert browser.iframe(id=compile(r'no_such_id')).exists is False
        assert browser.iframe(name='no_such_text').exists is False
        assert browser.iframe(name=compile(r'no_such_text')).exists is False
        assert browser.iframe(class_name='no_such_class').exists is False
        assert browser.iframe(class_name=compile(r'no_such_class')).exists is False
        assert browser.iframe(src='no_such_src').exists is False
        assert browser.iframe(src=compile(r'no_such_src')).exists is False
        assert browser.iframe(index=1337).exists is False
        assert browser.iframe(xpath="//iframe[@id='no_such_id']").exists is False

    def test_returns_true_if_an_element_in_an_iframe_does_exist(self, browser):
        assert browser.iframe().element(css='#senderElement').exists is True
        assert browser.iframe().element(id='senderElement').exists is True

    def test_returns_false_if_an_element_in_an_iframe_does_not_exist(self, browser):
        assert browser.iframe().element(css='#no_such_id').exists is False
        assert browser.iframe().element(id='no_such_id').exists is False

    def test_returns_true_if_an_element_outside_an_iframe_exists_after_checking_for_one_inside_that_does_exist(self, browser):
        existing_element = browser.element(css='#iframe_1')
        assert existing_element.exists is True
        assert browser.iframe().element(css='#senderElement').exists is True
        assert existing_element.exists is True

    def test_returns_true_if_an_element_outside_an_iframe_exists_after_checking_for_one_inside_that_does_not_exist(self, browser):
        existing_element = browser.element(css='#iframe_1')
        assert existing_element.exists is True
        assert browser.iframe().element(css='#no_such_id').exists is False
        assert existing_element.exists is True

    def test_returns_true_if_an_element_exists_in_a_frame_generated_in_a_collection(self, browser):
        assert browser.body().iframes()[0].div().exists is True

    def test_returns_false_for_sub_element_of_a_non_existing_frame(self, browser):
        assert browser.iframe(id='no_such_id').element().exists is False


class TestIFrameOther(object):
    @pytest.mark.page('nested_iframes.html')
    @pytest.mark.xfail_firefox(reason='https://bugzilla.mozilla.org/show_bug.cgi?id=1255946')
    def test_handles_nested_iframes(self, browser):
        from nerodia.wait.wait import Wait
        browser.iframe(id='two').iframe(id='three').link(id='four').click()

        Wait.until(lambda: browser.title == 'definition_lists')

    def test_raises_correct_exception_when_what_argument_is_invalid(self, browser):
        with pytest.raises(TypeError):
            browser.iframe(id=3.14).exists

    def test_handles_all_locators_for_element_which_does_not_exist(self, browser):
        assert browser.iframe(index=0).div(id='invalid').exists is False

    # present

    def test_returns_true_if_the_iframe_is_present(self, browser):
        assert browser.iframe(id='iframe_1').present is True

    def test_returns_false_if_the_iframe_is_not_present(self, browser):
        assert browser.iframe(id='no_such_id').present is False

    def test_switches_between_iframe_and_parent_when_needed(self, browser):
        for element in browser.iframe(id='iframe_1').elements():
            element.text
            browser.h1().text

    def test_switches_when_the_frame_is_created_by_subtype(self, browser):
        subtype = browser.iframe().to_subtype()
        subtype.iframe().locate()

    def test_switches_back_to_top_level_browsing_context(self, browser):
        browser.iframes()[0].ps().locate()
        assert browser.h1s()[0].text == 'Iframes'

    @pytest.mark.usefixtures('quick_timeout')
    def test_raises_correct_exception_when_accessing_elements_inside_non_existing_iframe(self, browser):
        with pytest.raises(UnknownFrameException):
            browser.iframe(name='no_such_name').p(index=0).id

    @pytest.mark.usefixtures('quick_timeout')
    def test_raises_correct_exception_when_accessing_a_non_existing_iframe(self, browser):
        with pytest.raises(UnknownFrameException):
            browser.iframe(name='no_such_name').id

    @pytest.mark.usefixtures('quick_timeout')
    def test_raises_correct_exception_when_accessing_a_non_existing_subiframe(self, browser):
        with pytest.raises(UnknownFrameException):
            browser.iframe(name='iframe1').iframe(name='no_such_name').id

    @pytest.mark.usefixtures('quick_timeout')
    def test_raises_correct_exception_when_accessing_a_non_existing_element_inside_an_existing_iframe(self, browser):
        with pytest.raises(UnknownObjectException):
            browser.iframe(index=1).p(index=1337).id

    def test_raises_correct_exception_when_trying_to_access_attributes_it_doesnt_have(self, browser):
        with pytest.raises(AttributeError):
            browser.iframe(index=0).foo

    def test_is_able_to_set_a_field(self, browser):
        browser.iframe(index=0).text_field(name='senderElement').set('new value')
        assert browser.iframe(index=0).text_field(name='senderElement').value == 'new value'

    @pytest.mark.usefixtures('quick_timeout')
    def test_will_suggest_looking_in_an_iframe_when_iframes_exist(self, browser):
        with pytest.raises(UnknownObjectException, match=r'.*Maybe look in an iframe?.*'):
            browser.text_field(name='senderElement').set('no')

    def test_will_suggest_looking_in_a_nested_iframe_when_iframes_exist(self, browser, page):
        browser.goto(page.url('nested_iframes.html'))
        top = browser.iframe(id='two')
        with pytest.raises(UnknownObjectException, match=r'.*Maybe look in an iframe?.*'):
            top.link(id='four').click()

    def test_executes_the_given_javascript_in_the_specified_iframe(self, browser):
        iframe = browser.iframe(index=0)
        assert iframe.div(id='set_by_js').text == ""
        iframe.execute_script("document.getElementById('set_by_js').innerHTML = "
                              "'Art consists of limitation. The most beautiful "
                              "part of every picture is the iframe.'")
        assert iframe.div(id='set_by_js').text == 'Art consists of limitation. The most ' \
                                                  'beautiful part of every picture is the iframe.'

    def test_returns_the_full_html_source_of_the_iframe(self, browser):
        assert '<title>iframe 1</title>' in browser.iframe().html.lower()

    def test_returns_the_text_inside_the_iframe(self, browser):
        assert 'Frame 1' in browser.iframe().text


class TestFramedDriver(object):
    def test_raises_attribute_error_if_method_is_not_defined_on_driver_or_element(self, browser):
        assert not hasattr(browser.iframe(id='iframe_1').wd, 'foo')
        with pytest.raises(AttributeError):
            browser.iframe(id='iframe_1').wd.foo

    def test_raises_exception_when_attempting_to_switch_to_a_non_frame_element(self, browser):
        from nerodia.elements.i_frame import FramedDriver
        element = browser.h1().wd
        fd = FramedDriver(element, browser)
        with pytest.raises(UnknownFrameException):
            fd.switch()
