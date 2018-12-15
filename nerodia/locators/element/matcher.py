import re
from itertools import islice

import nerodia
from nerodia.locators.class_helpers import ClassHelpers

try:
    from re import Pattern
except ImportError:
    from re import _pattern_type as Pattern


class Matcher(object):

    def __init__(self, query_scope, selector=None):
        self.query_scope = query_scope
        self.selector = selector or {}

    def match(self, elements, values_to_match, filter):
        elements = self._matching_labels(elements, values_to_match)
        return self._matching_elements(elements, values_to_match, filter=filter)

    # private

    def _matching_labels(self, elements, values_to_match):
        for key in ('label_element', 'visible_label_element'):
            label_value = values_to_match.pop(key, None)
            if not label_value:
                continue

            locator_key = key.replace('label', 'text').replace('_element', '')
            locator = {locator_key: label_value}
            return self._label_collection(elements, **locator)
        return elements

    def _label_collection(self, elements, **locator):
        from nerodia.elements.input import Input
        labels = []
        for label in self.query_scope.labels():
            if not self._elements_match(label.wd, locator):
                continue
            label_for = label.get_attribute('htmlFor')
            input = label.input() if label_for == '' else Input(self.query_scope, {'id': label_for})
            if input.wd in elements:
                labels.append(input.wd)
        return labels

    def _matching_elements(self, elements, values_to_match, filter='first'):
        if filter == 'first':
            idx = self._element_index(elements, values_to_match)
            counter = 0

            # Generator + slice to avoid fetching values for elements that will be discarded
            matches = []
            for element in elements:
                counter += 1
                if self._elements_match(element, values_to_match) is not False:
                    matches.append(element)
            try:
                val = list(islice(matches, idx + 1))[idx]
                nerodia.logger.debug('Iterated through {} elements to locate '
                                     '{}'.format(counter, self.selector))
                return val
            except IndexError:
                return None
        else:
            nerodia.logger.debug('Iterated through {} elements to locate all '
                                 '{}'.format(len(elements), self.selector))
            return [el for el in elements if self._elements_match(el, values_to_match)]

    def _elements_match(self, element, values_to_match):
        def check_match(how, expected):
            if how == 'tag_name':
                return self._validate_tag(element, expected)
            elif how in ['class', 'class_name']:
                value = self._fetch_value(element, how)
                return all(any(self._matches_values(class_value, match) for class_value
                               in value.split()) for match in ClassHelpers._flatten([expected]))
            else:
                return self._matches_values(self._fetch_value(element, how), expected)

        matches = all(check_match(how, expected) for how, expected in values_to_match.items())

        if values_to_match.get('text'):
            self._deprecate_text_regexp(element, values_to_match, matches)

        return matches

    def _matches_values(self, found, expected):
        if isinstance(expected, Pattern):
            return re.search(expected, found) is not None
        else:
            return expected == found

    def _fetch_value(self, element, how):
        if how in ('text', 'visible_text'):
            return element.text
        elif how == 'visible':
            return element.is_displayed()
        elif how == 'href':
            return element.get_attribute('href').strip()
        elif how in ['class', 'class_name']:
            return element.get_attribute(how).strip()
        else:
            if '__' in how:
                how.replace('__', '_')
            elif '_' in how:
                how.replace('_', '-')
            return element.get_attribute(how)

    def _element_index(self, elements, values_to_match):
        idx = values_to_match.pop('index', 0)
        if idx >= 0:
            return idx

        elements.reverse()
        return abs(idx) - 1

    def _validate_tag(self, element, tag_name):
        return self._matches_values(element.tag_name.lower(), tag_name)

    def _deprecate_text_regexp(self, element, selector, matches):
        from nerodia.elements.element import Element
        new_element = Element(self.query_scope, {'element': element})
        text_content = new_element.text_content
        if 'text' in selector:
            text_content_matches = re.search(selector.get('text'), text_content) is not None
        else:
            text_content_matches = None
        if not not text_content_matches == matches:
            return

        key = 'text' if 'text' in self.selector else 'label'
        selector_text = selector.get('text')
        dep = "Using '{}' locator with RegExp {} to match an element that includes " \
              "hidden text".format(key, selector_text)
        nerodia.logger.deprecate(dep, "'visible_{}'".format(key), ids=['text_regexp'])
