from re import compile

import pytest

from nerodia.exception import UnknownObjectException

pytestmark = pytest.mark.page('images.html')


class TestImageExist(object):
    def test_returns_true_if_the_element_exists(self, browser):
        assert browser.image(id='square').exists is True
        assert browser.image(id=compile(r'square')).exists is True
        assert browser.image(src='images/circle.png').exists is True
        assert browser.image(src=compile(r'circle')).exists is True
        assert browser.image(alt='circle').exists is True
        assert browser.image(alt=compile(r'cir')).exists is True
        assert browser.image(title='Circle').exists is True

    def test_returns_the_first_image_if_given_no_args(self, browser):
        assert browser.image().exists

    def test_returns_false_if_the_element_does_not_exist(self, browser):
        assert browser.image(id='no_such_id').exists is False
        assert browser.image(id=compile(r'no_such_id')).exists is False
        assert browser.image(src='no_such_src').exists is False
        assert browser.image(src=compile(r'no_such_src')).exists is False
        assert browser.image(alt='no_such_alt').exists is False
        assert browser.image(alt=compile(r'no_such_alt')).exists is False
        assert browser.image(title='no_such_title').exists is False
        assert browser.image(title=compile('no_such_title')).exists is False

    def test_raises_correct_exception_when_what_argument_is_invalid(self, browser):
        with pytest.raises(TypeError):
            browser.image(id=3.14).exists

    def test_raises_correct_exception_when_how_argument_is_invalid(self, browser):
        from nerodia.exception import MissingWayOfFindingObjectException
        with pytest.raises(MissingWayOfFindingObjectException):
            browser.image(no_such_how='some_value').exists


class TestImageAttributes(object):
    # alt
    def test_returns_the_alt_if_the_element_exists_and_has_alt(self, browser):
        assert browser.image(id='square').alt == 'square'
        assert browser.image(title='Circle').alt == 'circle'

    def test_returns_an_empty_string_if_the_image_exists_and_the_alt_doesnt(self, browser):
        assert browser.image(index=0).alt == ''

    def test_raises_correct_exception_for_alt_if_the_element_doesnt_exist(self, browser):
        with pytest.raises(UnknownObjectException):
            browser.image(index=1337).alt

    # id
    def test_returns_the_id_if_the_element_exists_and_has_id(self, browser):
        assert browser.image(title='Square').id == 'square'

    def test_returns_an_empty_string_if_the_image_exists_and_the_id_doesnt(self, browser):
        assert browser.image(index=0).id == ''

    def test_raises_correct_exception_for_id_if_the_element_doesnt_exist(self, browser):
        with pytest.raises(UnknownObjectException):
            browser.image(index=1337).id

    # src
    def test_returns_the_src_if_the_element_exists_and_has_src(self, browser):
        assert 'square.png' in browser.image(id='square').src
        assert browser.image(title='Square').id == 'square'

    def test_returns_an_empty_string_if_the_image_exists_and_the_src_doesnt(self, browser):
        assert browser.image(index=0).src == ''

    def test_raises_correct_exception_for_src_if_the_element_doesnt_exist(self, browser):
        with pytest.raises(UnknownObjectException):
            browser.image(index=1337).src

    # title
    def test_returns_the_title_if_the_element_exists(self, browser):
        assert browser.image(id='square').title == 'Square'

    def test_returns_an_empty_string_if_the_image_exists_and_the_title_doesnt(self, browser):
        assert browser.image(index=0).title == ''

    def test_raises_correct_exception_for_title_if_the_element_doesnt_exist(self, browser):
        with pytest.raises(UnknownObjectException):
            browser.image(index=1337).title


def test_finds_all_attribute_methods(browser):
    assert hasattr(browser.image(index=0), 'class_name')
    assert hasattr(browser.image(index=0), 'id')
    assert hasattr(browser.image(index=0), 'style')
    assert hasattr(browser.image(index=0), 'text')


def test_raises_correct_exception_when_the_image_doesnt_exist(browser):
    with pytest.raises(UnknownObjectException):
        browser.image(index=1337).click()


class TestImageOther(object):
    # height
    def test_returns_the_height_if_the_element_exists(self, browser):
        assert browser.image(id='square').height == 88

    def test_raises_correct_exception_for_height_if_the_element_doesnt_exist(self, browser):
        with pytest.raises(UnknownObjectException):
            browser.image(index=1337).height

    # width
    def test_returns_the_width_if_the_element_exists(self, browser):
        assert browser.image(id='square').width == 88

    def test_raises_correct_exception_for_width_if_the_element_doesnt_exist(self, browser):
        with pytest.raises(UnknownObjectException):
            browser.image(index=1337).width

    # loaded
    def test_returns_true_if_the_image_has_been_loaded(self, browser):
        assert browser.image(title='Circle').loaded
        assert browser.image(alt='circle').loaded
        assert browser.image(alt=compile('circle')).loaded

    def test_returns_false_if_the_image_has_not_been_loaded(self, browser):
        assert browser.image(id='no_such_file').loaded is False

    def test_raises_correct_exception_for_loaded_if_the_element_doesnt_exist(self, browser):
        with pytest.raises(UnknownObjectException):
            browser.image(index=1337).loaded
