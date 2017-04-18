class Screenshot(object):

    def __init__(self, driver):
        self.driver = driver

    def save(self, path):
        """
        Saves screenshot to given path
        :param path: file path

        :Example:

        browser.screenshot.save('screenshot.png')
        """
        self.driver.save_screenshot(path)

    def png(self):
        """
        Represents screenshot as PNG image string
        :rtype: str

        :Example:

        browser.screenshot.png
        #=> '\x95\xC7\x8C@1\xC07\x1C(Edb\x15\xB2\vL'
        """
        return self.driver.get_screenshot_as_png()

    def base64(self):
        """
        Represents screenshot as Base64 encoded string
        :rtype: str

        :Example:

        browser.screenshot.base64
        #=> '7HWJ43tZDscPleeUuPW6HhN3x+z7vU/lufmH0qNTtTum94IBWMT46evImci1vnFGT'
        """
        return self.driver.get_screenshot_as_base64()
