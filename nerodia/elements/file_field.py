from errno import ENOENT
from os import path

import six

from .html_elements import InputCollection
from .input import Input
from ..meta_elements import MetaHTMLElement


@six.add_metaclass(MetaHTMLElement)
class FileField(Input):
    def set(self, filepath):
        """
        Set the file field to the given path

        :param filepath: path to the file
        :raises: ENOENT
        """
        if not path.exists(filepath):
            raise OSError(ENOENT, '{!r} does not exist.'.format(filepath))
        self.value = filepath

    @property
    def value(self):
        """
        Gets teh value of the file field
        :rtype: str
        """
        return self.attribute_value('value')

    @value.setter
    def value(self, filepath):
        """
        Set the file field to the given path
        :param filepath: path to the file
        """
        self._element_call(lambda: self.el.send_keys(filepath))


@six.add_metaclass(MetaHTMLElement)
class FileFieldCollection(InputCollection):
    pass
