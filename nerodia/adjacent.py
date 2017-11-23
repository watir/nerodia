import re


class Adjacent(object):
    def parent(self, **kwargs):
        """
        Returns parent element of current element
        :rtype: nerodia.elements.elements.Element

        :Example:

        browser.text_field(name='new_user_field_name').parent() == browser.fieldset    #=> True
        """
        kwargs['index'] = kwargs.get('index', 0)
        return self._xpath_adjacent(**dict(kwargs, adjacent='ancestor', plural=False))

    def preceding_sibling(self, **kwargs):
        """
        Returns preceding sibling element of current element
        :rtype: nerodia.elements.elements.Element

        :Example:

        browser.text_field(name='new_user_first_name').preceding_sibling(index=1) == browser.legend
        #=> True
        """
        return self._xpath_adjacent(**dict(kwargs, adjacent='preceding', plural=False))

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
        return self._xpath_adjacent(**dict(kwargs, adjacent='preceding', plural=True))

    previous_siblings = preceding_siblings

    def following_sibling(self, **kwargs):
        """
        Returns following sibling element of current element
        :rtype: nerodia.elements.elements.Element

        :Example:

        browser.text_field(name='new_user_first_name').following_sibling(index=2) == \
            browser.text_field(id='new_user_last_name')    #=> True
        """
        return self._xpath_adjacent(**dict(kwargs, adjacent='following', plural=False))

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
        return self._xpath_adjacent(**dict(kwargs, adjacent='following', plural=True))

    next_siblings = following_siblings

    def siblings(self, **kwargs):
        """
        Returns collection of sibling elements of current element, including the current element
        :rtype: nerodia.element_collection.ElementCollection

        :Example:

        len(browser.text_field(name='new_user_first_name').siblings)    #=> 56
        """
        return self.parent().children(**kwargs)

    def child(self, **kwargs):
        """
        Returns element of direct child of current element
        :rtype: nerodia.elements.elements.Element

        :Example:

        browser.form(id='new_user').child == browser.fieldset    #=> True
        """
        return self._xpath_adjacent(**dict(kwargs, adjacent='child', plural=False))

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
        return self._xpath_adjacent(**dict(kwargs, adjacent='child', plural=True))

    # private

    def _xpath_adjacent(self, **kwargs):
        from .elements.html_elements import HTMLElement, HTMLElementCollection
        import nerodia

        plural = kwargs.pop('plural', None)
        index = kwargs.pop('index', None)
        tag_name = kwargs.get('tag_name')

        if not (plural or any(isinstance(val, re._pattern_type) for val in kwargs.values())):
            kwargs['index'] = index or 0

        if not plural and tag_name:
            klass = nerodia.tag_to_class.get(tag_name)
        elif not plural:
            klass = HTMLElement
        elif tag_name:
            klass = nerodia.tag_to_class.get('{}_collection'.format(tag_name))
        else:
            klass = HTMLElementCollection

        return klass(self, kwargs)
