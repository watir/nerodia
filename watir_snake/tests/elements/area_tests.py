import pytest
from re import compile

class TestAreaExist(object):

    def test_returns_true_if_the_area_exists(self, browser, page):
        page.load('images.html')
        assert browser.area(id='NCE').exists is True
        assert browser.area(id=compile(r'NCE')).exists is True
        assert browser.area(title='Tables').exists is True
        assert browser.area(title=compile(r'Tables')).exists is True

        # TODO: xfail IE
        assert browser.area(href='tables.html').exists is True

        assert browser.area(href=compile(r'tables')).exists is True

        assert browser.area(index=0).exists is True
        assert browser.area(xpath="//area[@id='NCE']").exists is True
