from ..element.selector_builder import SelectorBuilder as ElementSelectorBuilder,\
    XPath as ElementXPath


class SelectorBuilder(ElementSelectorBuilder):
    pass


class XPath(ElementXPath):

    def build(self, selector):
        if 'adjacent' in selector:
            return super(XPath, self).build(selector)

        wd_locator = super(XPath, self).build(selector)
        start_string = self.default_start
        tag_string = "[local-name()='th' or local-name()='td']"
        common_string = wd_locator['xpath'].replace(start_string, '')

        xpath = ''.join((start_string, tag_string, common_string))

        return {'xpath': xpath}

    @property
    def default_start(self):
        return './' if 'adjacent' in self.selector else './*'
