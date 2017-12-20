import six

from .html_elements import InputCollection
from .input import Input
from ..meta_elements import MetaHTMLElement


@six.add_metaclass(MetaHTMLElement)
class Radio(Input):
    def __init__(self, *args, **kwargs):
        super(Radio, self).__init__(*args, **kwargs)
        if 'text' in self.selector:
            self.selector['label'] = self.selector.pop('text')

    @property
    def is_set(self):
        """
        Returns True if the element is selected
        :rtype: bool
        """
        return self._element_call(lambda: self.el.is_selected())

    is_selected = is_set

    def set(self):
        """ Selects the radio input """
        if not self.is_set:
            self.click()

    select = set

    @property
    def text(self):
        lab = self.label()
        return lab.text if lab.exists else ''


@six.add_metaclass(MetaHTMLElement)
class RadioCollection(InputCollection):
    # private

    @property
    def _element_class(self):
        return Radio
