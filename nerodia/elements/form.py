import six

from .html_elements import HTMLElement
from ..meta_elements import MetaHTMLElement


@six.add_metaclass(MetaHTMLElement)
class Form(HTMLElement):
    def submit(self):
        self._element_call(lambda: self.el.submit(), self.wait_for_present)
        self.browser.after_hooks.run()
