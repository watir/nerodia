import six

from .html_elements import HTMLElement
from ..meta_elements import MetaHtmlElement


@six.add_metaclass(MetaHtmlElement)
class DList(HTMLElement):
    def to_dict(self):
        keys = [e.text for e in self.dts]
        values = [e.text for e in self.dds]
        return dict(zip(keys, values))
