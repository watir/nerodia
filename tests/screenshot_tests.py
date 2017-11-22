import base64

import pytest

PNG_HEADER = b'\211PNG'


@pytest.mark.page('wait.html')
class TestScreenshot(object):
    def test_gets_png_representation_of_screenshot(self, browser):
        assert browser.screenshot.png()[0:4] == PNG_HEADER

    def test_gets_base64_representation_of_screenshot(self, browser):
        image = browser.screenshot.base64()
        assert base64.b64decode(image)[0:4] == PNG_HEADER

    def test_saves_screenshot_to_given_file(self, browser):
        import tempfile
        tmp = tempfile.NamedTemporaryFile(suffix='.png')
        try:
            browser.screenshot.save(tmp.name)
            assert tmp.read()[0:4] == PNG_HEADER
        finally:
            tmp.close()
