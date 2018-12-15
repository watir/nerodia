from nerodia.exception import UnknownObjectException
from .radio import Radio, RadioCollection


class RadioSet(object):

    _name = None

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

    @property
    def exists(self):
        return self.source.exists

    @property
    def present(self):
        return self.source.present

    @property
    def visible(self):
        return self.source.visible

    @property
    def browser(self):
        return self.source.browser

    def assert_exists(self):
        return self.source.assert_exists()

    def radio(self, **kwargs):
        """
        Gets a Radio for the RadioSet
        :rtype: Radio
        """
        if self.name and ('name' not in kwargs or kwargs.get('name') == self.name):
            return self.frame.radio(**dict(kwargs, name=self.name))
        elif not self.name:
            return self.source
        else:
            raise UnknownObjectException('{} does not match name of RadioSet: '
                                         '{}'.format(kwargs.get('name'), self.name))

    def radios(self, **kwargs):
        """
        Gets a RadioCollection for the RadioSet
        :rtype: RadioCollection
        """
        if self.name and ('name' not in kwargs or kwargs.get('name') == self.name):
            return self._element_call(lambda: self.frame.radios(**dict(kwargs, name=self.name)),
                                      self.source.wait_for_present)
        elif not self.name:
            return self._single_radio_collection
        else:
            raise UnknownObjectException('{} does not match name of RadioSet: '
                                         '{}'.format(kwargs.get('name'), self.name))

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
        if self._name is None:
            self._name = self.source.name
        return self._name

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
        for key in ['value', 'label']:
            radio = self.radio(**{key: term})
            if radio.exists:
                if not radio.is_selected:
                    radio.click()
                return radio.value if key == 'value' else radio.text
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

        browser.radio_set(id='new_user_newsletter_yes') == \
            browser.radio_set(id='new_user_newsletter_yes')   #=> True
        browser.radio_set(id='new_user_newsletter_yes') == \
            browser.radio_set(id='new_user_newsletter_no')   #=> False
        """
        if not isinstance(other, RadioSet):
            return False
        return self.radios() == other.radios()

    def __getattr__(self, item):
        return getattr(self.source, item)

    # private

    def _element_call(self, *args, **kwargs):
        return self.source._element_call(*args, **kwargs)

    @property
    def _single_radio_collection(self):
        collection = RadioCollection(self.frame, self.source.selector)
        collection[0].cache = self.source.wd
        return collection
