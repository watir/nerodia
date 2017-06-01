from copy import copy
from inspect import stack


class Adjacent(object):
    def parent(self, **kwargs):
        """
        Returns parent element of current element
        :rtype: nerodia.elements.elements.Element

        :Example:

        browser.text_field(name='new_user_field_name').parent() == browser.fieldset    #=> True
        """
        kwargs['index'] = kwargs.get('index', 0)
        return self._xpath_adjacent('ancestor::', **kwargs)

    def preceding_sibling(self, **kwargs):
        """
        Returns preceding sibling element of current element
        :rtype: nerodia.elements.elements.Element

        :Example:

        browser.text_field(name='new_user_first_name').preceding_sibling(index=1) == browser.legend
        #=> True
        """
        kwargs['index'] = kwargs.get('index', 0)
        return self._xpath_adjacent('preceding-sibling::', **kwargs)

    previous_sibling = preceding_sibling

    def preceding_siblings(self, **kwargs):
        """
        Returns collection of preceding sibling elements of current element
        :rtype: nerodia.element_collection.ElementCollection

        :Example:

        len(browser.text_field(name='new_user_first_name').preceding_siblings)    #=> 3
        """
        if 'index' in kwargs:
            raise ValueError('#previous_siblings can not take an index value')
        return self._xpath_adjacent("preceding-sibling::", **kwargs)

    previous_siblings = preceding_siblings

    def following_sibling(self, **kwargs):
        """
        Returns following sibling element of current element
        :rtype: nerodia.elements.elements.Element

        :Example:

        browser.text_field(name='new_user_first_name').following_sibling(index=2) == \
            browser.text_field(id='new_user_last_name')    #=> True
        """
        kwargs['index'] = kwargs.get('index', 0)
        return self._xpath_adjacent('following-sibling::', **kwargs)

    next_sibling = following_sibling

    def following_siblings(self, **kwargs):
        """
        Returns collection of following sibling elements of current element
        :rtype: nerodia.element_collection.ElementCollection

        :Example:

        len(browser.text_field(name='new_user_first_name').following_siblings)    #=> 52
        """
        if 'index' in kwargs:
            raise ValueError('#following_siblings can not take an index value')
        return self._xpath_adjacent('following-sibling::', **kwargs)

    next_siblings = following_siblings

    def child(self, **kwargs):
        """
        Returns element of direct child of current element
        :rtype: nerodia.elements.elements.Element

        :Example:

        browser.form(id='new_user').child == browser.fieldset    #=> True
        """
        kwargs['index'] = kwargs.get('index', 0)
        return self._xpath_adjacent('', **kwargs)

    def children(self, **kwargs):
        """
        Returns collection of elements of direct children of current element
        :rtype: nerodia.element_collection.ElementCollection

        :Example:

        browser.select_list(id='new_user_languages').children == \
            browser.select_list(id='new_user_languages').options.to_list    #=> True
        """
        if 'index' in kwargs:
            raise ValueError('#children can not take an index value')
        return self._xpath_adjacent('', **kwargs)

    # private

    def _xpath_adjacent(self, direction='', **kwargs):
        from .elements.html_elements import HTMLElement, HTMLElementCollection
        import nerodia

        kwargs = copy(kwargs)
        index = kwargs.pop('index', None)
        tag_name = kwargs.pop('tag_name', '')
        if kwargs:
            caller = stack()[1][3]
            raise AttributeError('unsupported locators: {} for #{} method'.format(kwargs, caller))

        if index is not None:
            klass = nerodia.tag_to_class.get(tag_name) if tag_name else HTMLElement
            return klass(self, {'xpath': './{}{}[{}]'.format(direction, tag_name or '*', index + 1)})
        else:
            klass = nerodia.tag_to_class.get('{}_collection'.format(tag_name)) if tag_name else \
                HTMLElementCollection
            return klass(self, {'xpath': './{}{}'.format(direction, tag_name or '*')})
