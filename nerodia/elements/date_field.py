from datetime import date, datetime
from inspect import stack

import six
from dateutil import parser

from nerodia.elements.html_elements import InputCollection
from .input import Input
from ..meta_elements import MetaHTMLElement


@six.add_metaclass(MetaHTMLElement)
class DateField(Input):

    def js_set(self, value):
        """
        Set date field to the given date

        :param value: value to set to
        :type value: datetime or date or str

        :Example:

        browser.date_field(id='start_date').set('2018/01/31')

        """
        if isinstance(value, six.string_types):
            value = parser.parse(value, fuzzy=True)

        if not isinstance(value, (date, datetime)):
            raise TypeError('DateField#{} only accepts instances of date or '
                            'datetime'.format(stack()[0][3]))

        date_string = value.strftime('%Y-%m-%d')
        self._element_call(lambda: self._execute_js('setValue', self.el, date_string),
                           precondition=self.wait_for_writable)

    set = js_set

    @property
    def value(self):
        return self.attribute_value('value')

    @value.setter  # alias
    def value(self, *args):
        self.set(*args)


class DateFieldCollection(InputCollection):

    # private

    @property
    def _element_class(self):
        return DateField
