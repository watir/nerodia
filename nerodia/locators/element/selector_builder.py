import re
from collections import defaultdict
from importlib import import_module

import six

import nerodia
from nerodia.exception import LocatorException
from nerodia.locators import W3C_FINDERS
from nerodia.locators.class_helpers import ClassHelpers
from nerodia.locators.element.regexp_disassembler import RegexpDisassembler
from nerodia.locators.element.xpath_support import XpathSupport

try:
    from re import Pattern
except ImportError:
    from re import _pattern_type as Pattern

STRING_TYPES = [six.text_type, six.binary_type]
STRING_REGEX_TYPES = STRING_TYPES + [Pattern]

WHATS = {
    'adjacent': STRING_TYPES,
    'xpath': STRING_TYPES,
    'css': STRING_TYPES,
    'index': [int],
    'visible': [bool],
    'tag_name': STRING_REGEX_TYPES,
    'visible_text': STRING_REGEX_TYPES,
    'scope': [dict],
    'text': STRING_REGEX_TYPES
}


class SelectorBuilder(object):
    WILDCARD_ATTRIBUTE = re.compile(r'^(aria|data)_(.+)$')
    VALID_WHATS = defaultdict(lambda: STRING_REGEX_TYPES + [bool], WHATS)

    xpath_builder = None
    selector = None
    built = None

    def __init__(self, valid_attributes, query_scope):
        self.valid_attributes = valid_attributes
        self.custom_attributes = []
        self.query_scope = query_scope

    def build(self, selector):
        self.selector = selector
        self._deprecated_locators()
        self._normalize_selector()
        rep = repr(selector)
        from nerodia.browser import Browser
        scope = None
        if 'scope' not in self.selector and not isinstance(self.query_scope, Browser):
            scope = self.query_scope

        self.built = self.selector
        if self.wd_locator(self.selector.keys()) is None:
            self.built = self._build_wd_selector(self.selector)
        if 'index' in self.built and self.built['index'] == 0:
            self.built.pop('index')
        if scope is not None:
            self.built['scope'] = scope

        nerodia.logger.info('Converted {} to {}'.format(rep, self.built))

        return self.built

    def wd_locator(self, keys):
        intersect = list(set(W3C_FINDERS).intersection(set(keys)))
        if intersect:
            return intersect[0]

    # private

    def _normalize_selector(self):
        wd_locators = set(self.selector.keys()).intersection(W3C_FINDERS)
        if len(wd_locators) > 1:
            raise LocatorException('Can not locate element with {}'.format(wd_locators))

        if self._use_scope:
            self.selector['scope'] = self.query_scope.selector_builder.built

        if 'class' in self.selector or 'class_name' in self.selector:
            classes = [self.selector.get('class')]
            classes.extend([self.selector.pop('class_name', None)])
            classes = list(_ for _ in ClassHelpers._flatten(classes) if _ is not None)

            for class_name in classes:
                if isinstance(class_name, tuple(STRING_TYPES)) and ' ' in class_name.strip():
                    self._deprecate_class_list(class_name)

            self.selector['class'] = classes

        if self.selector.get('adjacent') == 'ancestor' and 'text' in self.selector:
            raise LocatorException('Can not find parent element with text locator')

        for key in self.selector.copy():
            self._check_type(key, self.selector.get(key))
            how, what = self._normalize_locator(key, self.selector.pop(key, None))
            self.selector[how] = what

    @property
    def _use_scope(self):
        from nerodia.elements.i_frame import IFrame
        from nerodia.browser import Browser
        w3c_cpy = set(W3C_FINDERS)
        w3c_cpy.add('adjacent')
        if len(set(self.selector.keys()).intersection(w3c_cpy)) > 0:
            return False

        if isinstance(self.query_scope, (Browser, IFrame)):
            return False

        scope_invalid_locators = [x for x in self.query_scope.selector_builder.built.keys() if
              x != self._implementation_locator]

        return len(scope_invalid_locators) == 0

    def _deprecate_class_list(self, class_name):
        dep = "Using the 'class' locator to locate multiple classes with a String value " \
              "(i.e. '{}')".format(class_name)
        nerodia.logger.deprecate(dep, 'list (e.g. {})'.format(class_name.split()),
                                 ids=['class_list'])

    def _check_type(self, how, what):
        if how in ['class', 'class_name']:
            for c in list(ClassHelpers._flatten([what])):
                self._raise_unless(c, self.VALID_WHATS[how])
        else:
            self._raise_unless(what, self.VALID_WHATS[how])

    @property
    def should_use_label_element(self):
        return not self._is_valid_attribute('label')

    def _normalize_locator(self, how, what):
        if how in ('tag_name', 'text', 'xpath', 'index', 'css', 'visible', 'visible_text',
                   'adjacent'):
            # include 'class' since the valid attribute is 'class_name'
            return [how, what]
        elif how in ('label', 'visible_label'):
            if self.should_use_label_element:
                return ['{}_element'.format(how), what]
            else:
                return [how, what]
        elif how in ('class_name', 'class'):
            if isinstance(what, list):
                what = [_ for _ in what if _ != '']
                if len(what) == 0:
                    what = False
            return ['class', what]
        elif how == 'link':
            return ['link_text', what]
        elif how == 'caption':
            # This allows any element to be located with 'caption' instead of 'text'
            # It is deprecated because caption is a valid attribute on a Table
            # It is also a valid Element, so it also needs to be removed from the Table attributes
            # list
            nerodia.logger.deprecate("Locating elements with 'caption'", "'text' locator",
                                     ids=['caption'])
            return ['text', what]
        else:
            self._check_custom_attribute(how)
            return [how, what]

    def _check_custom_attribute(self, attribute):
        if self._is_valid_attribute(attribute) or self.WILDCARD_ATTRIBUTE.search(attribute):
            return None
        self.custom_attributes.append(attribute)

    # Extensions implement this method when creating a different selector builder
    @property
    def _implementation_class(self):
        try:
            mod = import_module(self.__module__)
            xpath = getattr(mod, 'XPath', XPath)
        except ImportError:
            xpath = XPath
        return xpath

    def _build_wd_selector(self, selector):
        return self._implementation_class().build(selector)

    @property
    def _implementation_locator(self):
        return self._implementation_class.LOCATOR

    def _is_valid_attribute(self, attribute):
        return self.valid_attributes and attribute in self.valid_attributes

    @staticmethod
    def _combine_with_xpath_or_css(selector):
        keys = list(selector)
        keys = [x for x in keys if x not in ['visible', 'visible_text', 'index']]

        if len(set(keys) - {'tag_name'}) == 0:
            return True
        elif selector.get('tag_name') == 'input' and set(keys) == {'tag_name', 'type'}:
            return True
        else:
            return False

    @staticmethod
    def _raise_unless(what, types):
        if what.__class__ in types:
            return

        raise TypeError('expected one of {!r}, got {!r}:{}'.format(types, what, what.__class__))

    def _deprecated_locators(self):
        for locator in ('partial_link_text', 'link_text', 'link'):
            if locator not in self.selector:
                continue

            nerodia.logger.deprecate('{!r} locator'.format(locator), 'visible_text',
                                     ids=['link_text'])
            tag = self.selector.get('tag_name')
            if tag is None or tag == 'a':
                continue
            raise LocatorException('Can not use {} locator to find a {} '
                                   'element'.format(locator, tag))


class XPath(object):
    CAN_NOT_BUILD = ['visible', 'visible_text', 'visible_label_element']

    LOCATOR = 'xpath'

    built = None
    selector = None
    requires_matches = None
    adjacent = None

    def build(self, selector):
        self.selector = selector

        self.built = {}

        for key in self.selector.copy():
            if key in self.CAN_NOT_BUILD:
                self.built[key] = self.selector.pop(key)

        index = self.selector.pop('index', None)
        self.adjacent = self.selector.pop('adjacent', None)
        self.scope = self.selector.pop('scope', None)

        xpath = self._start_string
        xpath += self._adjacent_string
        xpath += self._tag_string
        xpath += self._class_string
        xpath += self._text_string
        xpath += self._additional_string
        xpath += self._label_element_string
        xpath += self._attribute_string

        self.built['xpath'] = self._add_index(xpath, index) if index is not None else xpath

        return self.built

    # private

    def _process_attribute(self, key, value):
        if isinstance(value, Pattern):
            return self._predicate_conversion(key, value)
        else:
            return self._predicate_expression(key, value)

    def _predicate_expression(self, key, val):
        if val is True:
            return self._attribute_presence(key)
        elif val is False:
            return self._attribute_absence(key)
        else:
            return self._equal_pair(key, val)

    def _predicate_conversion(self, key, regexp):
        lower = key == 'type' or regexp.flags & re.IGNORECASE == re.IGNORECASE

        lhs = self._lhs_for(key, lower)
        results = RegexpDisassembler(regexp).substrings

        if len(results) == 0:
            self._add_to_matching(key, regexp)
            return lhs
        elif len(results) == 1 and self._starts_with(results, regexp) and not self._is_visible:
            return "starts-with({}, '{}')".format(lhs, results[0])

        self._add_to_matching(key, regexp, results)

        return ' and '.join(("contains({}, '{}')".format(lhs, substring) for substring in results))

    @property
    def _start_string(self):
        start = './' if self.adjacent is not None else './/*'
        if self.scope is not None:
            return '({})[1]{}'.format(self.scope['xpath'], start.replace('.', ''))
        else:
            return start

    @property
    def _adjacent_string(self):
        if self.adjacent is None:
            return ''
        elif self.adjacent == 'ancestor':
            return 'ancestor::*'
        elif self.adjacent == 'preceding':
            return 'preceding-sibling::*'
        elif self.adjacent == 'following':
            return 'following-sibling::*'
        elif self.adjacent == 'child':
            return 'child::*'
        else:
            raise LocatorException('Unable to process adjacent locator with '
                                   '{}'.format(self.adjacent))

    @property
    def _tag_string(self):
        tag_name = self.selector.pop('tag_name', None)
        if tag_name is None:
            return ''
        else:
            return '[{}]'.format(self._process_attribute('tag_name', tag_name))

    @property
    def _class_string(self):
        from nerodia.locators.class_helpers import ClassHelpers
        class_name = self.selector.pop('class', None)
        if class_name is None:
            return ''

        self.built['class'] = []

        predicates = []
        for value in ClassHelpers._flatten([class_name]):
            pred = self._process_attribute('class', value)
            if pred is not None:
                predicates.append(pred)

        if len(self.built['class']) == 0:
            self.built.pop('class')

        if len(predicates) > 0:
            return '[{}]'.format(' and '.join(predicates))
        else:
            return ''

    @property
    def _text_string(self):
        text = self.selector.pop('text', None)
        if text is None:
            return ''
        elif isinstance(text, Pattern):
            self.built['text'] = text
            return ''
        else:
            return '[{}]'.format(self._predicate_expression('text', text))

    @property
    def _label_element_string(self):
        label = self.selector.pop('label_element', None)
        if label is None:
            return ''

        key = 'contains_text' if isinstance(label, Pattern) else 'text'

        value = self._process_attribute(key, label)

        if 'contains_text' in self.built:
            self.built['label_element'] = self.built.pop('contains_text')

        # TODO: This conditional can be removed when we remove this deprecation
        if isinstance(label, Pattern):
            self.built['label_element'] = label
            return ''
        else:
            return "[@id=//label[{0}]/@for or parent::label[{0}]]".format(value)

    @property
    def _attribute_string(self):
        attributes = []
        for key in self.selector.copy():
            attribute = self._process_attribute(key, self.selector.pop(key))
            if attribute is not None:
                attributes.append(attribute)
        attributes = list(ClassHelpers._flatten(attributes))

        return '[{}]'.format(' and '.join(attributes)) if len(attributes) > 0 else ''

    @property
    def _additional_string(self):
        # to be used by subclasses as necessary
        return ''

    def _add_index(self, xpath, index=None):
        if self.adjacent is not None:
            return '{}[{}]'.format(xpath, index + 1)
        elif index and index >= 0 and len(self.built) == 0:
            return '({})[{}]'.format(xpath, index + 1)
        elif index and index < 0 and len(self.built) == 0:
            last_value = 'last()'
            if index < -1:
                last_value += str(index + 1)
            return '({})[{}]'.format(xpath, last_value)
        else:
            self.built['index'] = index
            return xpath

    @property
    def _is_visible(self):
        return not not set(self.built).intersection(XPath.CAN_NOT_BUILD)

    def _starts_with(self, results, regexp):
        return regexp.pattern.startswith('^') and results[0] == regexp.pattern[1:]

    def _add_to_matching(self, key, regexp, results=None):
        if results is None or self._requires_matching(results, regexp):
            if key == 'class':
                self.built[key].append(regexp)
            else:
                self.built[key] = regexp

    def _requires_matching(self, results, regexp):
        if regexp.flags & re.IGNORECASE == re.IGNORECASE:
            return results[0].lower() != regexp.pattern.lower()
        else:
            return results[0] != regexp.pattern

    @staticmethod
    def _lhs_for(key, lower=False):
        if key == 'tag_name':
            return 'local-name()'
        elif key == 'href':
            return 'normalize-space(@href)'
        elif key == 'text':
            return 'normalize-space()'
        elif key == 'contains_text':
            return 'text()'
        elif isinstance(key, str):
            if '__' in key:
                lhs = '@{}'.format(key.replace('__', '_'))
            else:
                lhs = '@{}'.format(key.replace('_', '-'))
            return XpathSupport.lower(lhs) if lower else lhs
        else:
            raise LocatorException('Unable to build XPath using {}:{}'.format(key, key.__class__))

    def _attribute_presence(self, attribute):
        return self._lhs_for(attribute)

    def _attribute_absence(self, attribute):
        return 'not({})'.format(self._lhs_for(attribute))

    def _equal_pair(self, key, value):
        if key == 'class':
            if re.search(r'^!', value):
                value = value[1:]
                negate_xpath = True
            else:
                negate_xpath = False
            expression = "contains(concat(' ', @class, ' '), " \
                         "{})".format(XpathSupport.escape(' {} '.format(value)))
            return "not({})".format(expression) if negate_xpath else expression
        else:
            return "{}={}".format(self._lhs_for(key, key == 'type'), XpathSupport.escape(value))
