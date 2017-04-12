import six

from .html_elements import HTMLElement
from ..meta_element import MetaElement


@six.add_metaclass(MetaElement)
class Form(HTMLElement):
    def submit(self):
        self._element_call(lambda _: self.element.submit, self._wait_for_present)
        # browser.after_hooks.run()  # TODO
