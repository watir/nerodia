import six

from .html_elements import HTMLElement
from ..meta_elements import MetaHtmlElement


@six.add_metaclass(MetaHtmlElement)
class Area(HTMLElement):
    _attr_href = (str, 'href')
