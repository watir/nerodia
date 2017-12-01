from re import compile

import pytest

from nerodia.exception import UnknownFrameException, UnknownObjectException

pytestmark = pytest.mark.page('frames.html')


def test_handles_cross_frame_javascript(browser):
    assert browser.frame(id='frame_1').text_field(name='senderElement').value == 'send_this_value'
    assert browser.frame(id='frame_2').text_field(name='recieverElement').value == 'old_value'
    browser.frame(id='frame_1').button(id='send').click()
    assert browser.frame(id='frame_2').text_field(name='recieverElement').value == 'send_this_value'


class TestFrameExist(object):
    def test_returns_true_if_the_frame_exists(self, browser):
        assert browser.frame(id='frame_1').exists is True
        assert browser.frame(id=compile(r'frame')).exists is True
        assert browser.frame(name='frame1').exists is True
        assert browser.frame(name=compile(r'frame')).exists is True
        assert browser.frame(class_name='half').exists is True
        assert browser.frame(class_name=compile(r'half')).exists is True
        assert browser.frame(src='frame_1.html').exists is True
        assert browser.frame(src=compile(r'frame_1')).exists is True
        assert browser.frame(index=0).exists is True
        assert browser.frame(xpath="//frame[@id='frame_1']").exists is True

    def test_returns_the_first_frame_if_given_no_args(self, browser):
        assert browser.frame().exists

    def test_returns_false_if_the_frame_does_not_exist(self, browser):
        assert browser.frame(id='no_such_id').exists is False
        assert browser.frame(id=compile(r'no_such_id')).exists is False
        assert browser.frame(name='no_such_text').exists is False
        assert browser.frame(name=compile(r'no_such_text')).exists is False
        assert browser.frame(class_name='no_such_class').exists is False
        assert browser.frame(class_name=compile(r'no_such_class')).exists is False
        assert browser.frame(src='no_such_src').exists is False
        assert browser.frame(src=compile(r'no_such_src')).exists is False
        assert browser.frame(index=1337).exists is False
        assert browser.frame(xpath="//frame[@id='no_such_id']").exists is False


class TestFrameOther(object):
    @pytest.mark.page('nested_frames.html')
    @pytest.mark.xfail_firefox(reason='https://bugzilla.mozilla.org/show_bug.cgi?id=1255946')
    def test_handles_nested_frames(self, browser):
        from nerodia.wait.wait import Wait
        browser.frame(id='two').frame(id='three').link(id='four').click()

        Wait.until(lambda: browser.title == 'definition_lists')

    def test_raises_correct_exception_when_what_argument_is_invalid(self, browser):
        with pytest.raises(TypeError):
            browser.frame(id=3.14).exists

    def test_raises_correct_exception_when_how_argument_is_invalid(self, browser):
        from nerodia.exception import MissingWayOfFindingObjectException
        with pytest.raises(MissingWayOfFindingObjectException):
            browser.frame(no_such_how='some_value').exists

    def test_raises_correct_exception_when_accessing_elements_inside_non_existing_frame(self, browser):
        with pytest.raises(UnknownFrameException):
            browser.frame(name='no_such_name').p(index=0).id

    def test_raises_correct_exception_when_accessing_a_non_existing_frame(self, browser):
        with pytest.raises(UnknownFrameException):
            browser.frame(name='no_such_name').id

    def test_raises_correct_exception_when_accessing_a_non_existing_subframe(self, browser):
        with pytest.raises(UnknownFrameException):
            browser.frame(name='frame1').frame(name='no_such_name').id

    def test_raises_correct_exception_when_accessing_a_non_existing_element_inside_an_existing_frame(self, browser):
        with pytest.raises(UnknownObjectException):
            browser.frame(index=1).p(index=1337).id

    def test_raises_correct_exception_when_trying_to_access_attributes_it_doesnt_have(self, browser):
        with pytest.raises(AttributeError):
            browser.frame(index=0).foo

    def test_is_able_to_set_a_field(self, browser):
        browser.frame(index=0).text_field(name='senderElement').set('new value')
        assert browser.frame(index=0).text_field(name='senderElement').value == 'new value'

    def test_can_access_the_frames_parent_element_after_use(self, browser):
        el = browser.frameset()
        el.frame().text_field().value
        assert isinstance(el.attribute_value('cols'), str)

    def test_executes_the_given_javascript_in_the_specified_frame(self, browser):
        frame = browser.frame(index=0)
        assert frame.div(id='set_by_js').text == ""
        frame.execute_script("document.getElementById('set_by_js').innerHTML = "
                             "'Art consists of limitation. The most beautiful "
                             "part of every picture is the frame.'")
        assert frame.div(id='set_by_js').text == 'Art consists of limitation. The most beautiful ' \
                                                 'part of every picture is the frame.'

    def test_returns_the_full_html_source_of_the_frame(self, browser):
        assert '<title>frame 1</title>' in browser.frame().html.lower()
