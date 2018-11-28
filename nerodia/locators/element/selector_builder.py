import inspect
import re
from copy import copy
from importlib import import_module

import six
from selenium.webdriver.common.by import By

import nerodia
from nerodia.exception import LocatorException
from nerodia.locators.class_helpers import ClassHelpers
from nerodia.locators.element.regexp_disassembler import RegexpDisassembler
from nerodia.locators.element.xpath_support import XpathSupport

try:
    from re import Pattern
except ImportError:
    from re import _pattern_type as Pattern

STRING_TYPES = [six.text_type, six.binary_type]


class SelectorBuilder(object):
    VALID_WHATS = [Pattern, bool] + STRING_TYPES
    WILDCARD_ATTRIBUTE = re.compile(r'^(aria|data)_(.+)$')

    def __init__(self, valid_attributes):
        self.valid_attributes = valid_attributes
        self.custom_attributes = []
        self.xpath_builder = None
        self.selector = None

    def build(self, selector):
        rep = repr(selector)
        self.selector = selector
        self.normalize_selector()

        xpath_css = {}

        for key in copy(self.selector):
            if key in ['xpath', 'css']:
                xpath_css[key] = self.selector.pop(key)

        if len(xpath_css) == 0:
            built = self._build_wd_selector(self.selector)
        else:
            self._process_xpath_css(xpath_css)
            built = xpath_css

        if self.selector.get('index') == 0:
            self.selector.pop('index')

        nerodia.logger.debug('Converted {} to {}, with {} '
                             'to match'.format(rep, built, self.selector))
        return [built, self.selector]

    def normalize_selector(self):
        if self.selector.get('adjacent') == 'ancestor' and 'text' in self.selector:
            raise LocatorException('Can not find parent element with text locator')

        for key in self.selector.copy():
            self.check_type(key, self.selector.get(key))
            how, what = self._normalize_locator(key, self.selector.pop(key, None))
            self.selector[how] = what

    def check_type(self, how, what):
        if how in ['adjacent', 'xpath', 'css']:
            return self._raise_unless(what, str)
        elif how == 'index':
            return self._raise_unless(what, int)
        elif how == 'visible':
            return self._raise_unless(what, bool)
        elif how in ['tag_name', 'visible_text', 'text']:
            return self._raise_unless(what, 'string_or_regexp')
        elif how in ['class', 'class_name']:
            if isinstance(what, list):
                if len(what) == 0:
                    raise LocatorException("Cannot locate elements with an empty list for "
                                           "'class_name'")

                for w in what:
                    self._raise_unless(w, 'string_or_regexp')
                return
        if type(what) not in self.VALID_WHATS:
            raise TypeError(
                'expected one of {}, got {!r}:{}'.format(self.VALID_WHATS, what, what.__class__))

    @property
    def should_use_label_element(self):
        return not self._is_valid_attribute('label')

    # private

    def _normalize_locator(self, how, what):
        if how in ['tag_name', 'text', 'xpath', 'index', 'class', 'css', 'visible', 'visible_text',
                   'adjacent']:
            # include 'class' since the valid attribute is 'class_name'
            return [how, what]
        elif how == 'label':
            if self.should_use_label_element:
                return ['{}_element'.format(how), what]
            else:
                return [how, what]
        elif how == 'class_name':
            return ['class', what]
        elif how == 'caption':
            # This allows any element to be located with 'caption' instead of 'text'
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

    def _process_xpath_css(self, xpath_css):
        if len(xpath_css) > 1:
            raise LocatorException("'xpath' and 'css' cannot be combined ({})".format(xpath_css))

        if self._combine_with_xpath_or_css(self.selector):
            return

        raise LocatorException("{} cannot be combined with all of these locators "
                               "({})".format(list(xpath_css)[0], self.selector))

    # Implement this method when creating a different selector builder
    def _build_wd_selector(self, selector):
        try:
            mod = import_module(self.__module__)
            xpath = getattr(mod, 'XPath', XPath)
        except ImportError:
            xpath = XPath
        return xpath().build(selector)

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
    def _raise_unless(what, typ):
        if typ == bool and isinstance(what, bool):
                return
        elif typ == 'string_or_regexp' and \
                type(what) in [six.text_type, six.binary_type, Pattern]:
            return
        elif inspect.isclass(typ):
            typ_check = (six.text_type, six.string_types) if typ == str else typ
            if isinstance(what, typ_check):
                return

        raise TypeError('expected {}, got {!r}:{}'.format(typ, what, what.__class__))


class XPath(object):
    CAN_NOT_BUILD = ['visible', 'visible_text']

    def __init__(self):
        self.selector = None
        self.requires_matches = None
        self.adjacent = None

    def build(self, selector):
        self.selector = selector

        self.requires_matches = {}

        for key in self.selector.copy():
            if key in self.CAN_NOT_BUILD:
                self.requires_matches[key] = self.selector.pop(key)

        index = self.selector.pop('index', None)
        self.adjacent = self.selector.pop('adjacent', None)

        xpath = self._start_string
        xpath += self._adjacent_string
        xpath += self._tag_string
        xpath += self._class_string
        xpath += self._text_string
        xpath += self._additional_string
        xpath += self._attribute_string

        if index is not None:
            xpath = self._add_index(xpath, index)

        self.selector.update(self.requires_matches)

        return {By.XPATH: xpath}

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
        return './' if self.adjacent is not None else './/*'

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

        if isinstance(class_name, str) and ' ' in class_name.strip():
            self._deprecate_class_list(class_name)

        self.requires_matches['class'] = []

        predicates = []
        for value in ClassHelpers._flatten([class_name]):
            pred = self._process_attribute('class', value)
            if pred is not None:
                predicates.append(pred)

        if len(self.requires_matches['class']) == 0:
            self.requires_matches.pop('class')

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
            self.requires_matches['text'] = text
            return ''
        else:
            return '[{}]'.format(self._predicate_expression('text', text))

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
        elif index and index >= 0 and len(self.requires_matches) == 0:
            return '({})[{}]'.format(xpath, index + 1)
        elif index and index < 0 and len(self.requires_matches) == 0:
            last_value = 'last()'
            if index < -1:
                last_value += str(index + 1)
            return '({})[{}]'.format(xpath, last_value)
        else:
            self.requires_matches['index'] = index
            return xpath

    def _deprecate_class_list(self, class_name):
        dep = "Using the 'class' locator to locate multiple classes with a String value " \
              "(i.e. '{}')".format(class_name)
        nerodia.logger.deprecate(dep, 'list (e.g. {})'.format(class_name.split()),
                                 ids=['class_list'])

    @property
    def _is_visible(self):
        return not not set(self.requires_matches).intersection(XPath.CAN_NOT_BUILD)

    def _starts_with(self, results, regexp):
        return regexp.pattern.startswith('^') and results[0] == regexp.pattern[1:]

    def _add_to_matching(self, key, regexp, results=None):
        if results is None or self._requires_matching(results, regexp):
            if key == 'class':
                self.requires_matches[key].append(regexp)
            else:
                self.requires_matches[key] = regexp

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
        if key == 'label_element':
            # we assume 'label' means a corresponding label element, not the attribute
            text = "{}={}".format(self._lhs_for('text'), XpathSupport.escape(value))
            return "(@id=//label[{0}]/@for or parent::label[{0}])".format(text)
        elif key == 'class':
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
