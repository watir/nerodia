import datetime
from inspect import stack

import six
from dateutil import parser

from nerodia.elements.html_elements import InputCollection
from .input import Input
from ..meta_elements import MetaHTMLElement


@six.add_metaclass(MetaHTMLElement)
class DateTimeField(Input):

    def js_set(self, value):
        """
        Set datetime field to the given date and time

        :param value: value to set to
        :type value: datetime or str

        :Example:

        browser.date_time_field(id='start_date').set('2018/01/31 14:00')

        """
        if isinstance(value, (float, int)):
            value = datetime.datetime.fromtimestamp(value)

        if isinstance(value, datetime.time):
            value = datetime.datetime.combine(datetime.date.today(), value)

        if isinstance(value, six.string_types):
            value = parser.parse(value, fuzzy=True)

        if not isinstance(value, datetime.datetime):
            raise TypeError('DateTimeField#{} only accepts instances of datetime or '
                            'time'.format(stack()[0][3]))

        date_time_string = value.strftime('%Y-%m-%dT%H:%M')
        self._element_call(lambda: self._execute_js('setValue', self.el, date_time_string),
                           precondition=self.wait_for_writable)

    set = js_set

    @property
    def value(self):
        return self.attribute_value('value')

    @value.setter  # alias
    def value(self, *args):
        self.set(*args)


class DateTimeFieldCollection(InputCollection):

    # private

    @property
    def _element_class(self):
        return DateTimeField
