from nerodia.exception import UnknownObjectException
from .radio import Radio, RadioCollection


class RadioSet(object):
    def __init__(self, query_scope, selector):
        if not isinstance(selector, dict):
            raise ValueError('invalid argument: {}'.format(selector))

        self.source = Radio(query_scope, selector)
        self.frame = self.source.parent(tag_name='form')

    def __iter__(self):
        """
        Yields each Radio associated with this set

        :rtype: iter

        :Example:

        radio_set = browser.radio_set(id='some_radio_set')
        for radio in radio_set:
            print(radio.text)
        """
        for e in self.radios():
            yield e

    def __len__(self):
        """
        Returns the number of Radios in the RadioSet
        :rtype: int
        """
        return len(self.radios())

    def __getitem__(self, idx):
        """
        Get the Radio at the given index in the RadioSet

        :param idx: index of Radio element, 0-indexed
        :type idx: int
        :return: instance of Radio
        :rtype: nerodia.elements.radio.Radio
        """
        return self.radios()[idx]

    def radio(self, **kwargs):
        """
        Gets a Radio for the RadioSet
        :rtype: Radio
        """
        name = self.name
        if name and ('name' not in kwargs or kwargs.get('name') == name):
            return self.frame.radio(**dict(kwargs, name=name))
        elif not name:
            return self.source
        else:
            raise UnknownObjectException('{} does not match name of RadioSet: '
                                         '{}'.format(kwargs.get('name'), name))

    def radios(self, **kwargs):
        """
        Gets a RadioCollection for the RadioSet
        :rtype: RadioCollection
        """
        name = self.name
        if name and ('name' not in kwargs or kwargs.get('name') == name):
            return self._element_call(lambda: self.frame.radios(**dict(kwargs, name=name)),
                                      self.source.wait_for_present)
        elif not name:
            return RadioCollection(self.frame, {'element': self.source.wd})
        else:
            raise UnknownObjectException('{} does not match name of RadioSet: '
                                         '{}'.format(kwargs.get('name'), name))

    @property
    def enabled(self):
        """
        Returns True if any radio buttons in the set are enabled

        :rtype: bool
        """
        return any(e.enabled for e in self)

    @property
    def disabled(self):
        """
        Returns True if all radio buttons in the set are disabled

        :rtype: bool
        """
        return not self.enabled

    @property
    def name(self):
        """
        Returns the name attribute for the set

        :rtype: str
        """
        return self.source.name

    @property
    def type(self):
        """
        Returns the name attribute for the set

        :rtype: str
        """
        self.source.assert_exists()
        return 'radio'

    def includes(self, term):
        """
        Returns True if the radio set has one ore more radio buttons where label matches the given
        value

        :rtype: bool
        """
        return self.radio(label=term).exists

    def select(self, term):
        """
        Select the radio button whose value or label matches the given string.

        :param term: string or regex
        :returns: the value or text of the radio selected
        :rtype: str
        """
        found_by_value = self.radio(value=term)
        found_by_text = self.radio(label=term)

        if found_by_value.exists:
            if not found_by_value.is_selected:
                found_by_value.click()
            return found_by_value.value
        elif found_by_text.exists:
            if not found_by_text.is_selected:
                found_by_text.click()
            return found_by_text.text
        else:
            raise UnknownObjectException('Unable to locate radio matching {}'.format(term))

    def is_selected(self, term):
        """
        Returns True if the radio button found matching the term is selected

        :param term: string or regex
        :rtype: bool
        """
        found = self.frame.radio(label=term)
        if found.exists:
            return found.is_selected
        raise UnknownObjectException('Unable to locate radio matching {}'.format(term))

    @property
    def selected(self):
        """
        Returns the selected Radio element
        Returns None if no radio button is selected
        :rtype: Radio or None
        """
        return next((el for el in self if el.is_selected), None)

    @property
    def value(self):
        """
        Returns the value of the selected radio button in the set.
        Returns None if no radio button is selected
        :rtype: str or None
        """
        sel = self.selected
        return sel and sel.value

    @property
    def text(self):
        """
        Returns the text of the selected radio button in the set.
        Returns None if no radio button is selected
        :rtype: str or None
        """
        sel = self.selected
        return sel and sel.text

    def __eq__(self, other):
        """
        Returns True if two RadioSets are equal.

        :param other: other RadioSet
        :rtype: bool

        :Example:

        browser.radio_set(id='new_user_newsletter_yes') == browser.radio_set(id='new_user_newsletter_yes')   #=> True
        browser.radio_set(id='new_user_newsletter_yes') == browser.radio_set(id='new_user_newsletter_no')   #=> False
        """
        if not isinstance(other, RadioSet):
            return False
        return self.radios() == other.radios()

    def __getattr__(self, item):
        return getattr(self.source, item)

    # private

    def _element_call(self, method, exist_check=None):
        return self.source._element_call(method, exist_check)
