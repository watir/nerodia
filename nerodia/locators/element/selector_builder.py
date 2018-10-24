import inspect
import re
from copy import copy
from importlib import import_module

import six
from selenium.webdriver.common.by import By

import nerodia
from nerodia.exception import LocatorException
from ...xpath_support import XpathSupport

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

        for key in self.selector:
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

    def _raise_unless(self, what, klass):
        if klass == bool and isinstance(what, bool):
                return
        elif klass == 'string_or_regexp' and \
                type(what) in [six.text_type, six.binary_type, Pattern]:
            return
        elif inspect.isclass(klass) and isinstance(what, klass):
            return

        raise TypeError('expected {}, got {!r}:{}'.format(klass, what, what.__class__))


class XPath(object):
    CAN_NOT_BUILD = ['visible', 'visible_text']

    def __init__(self):
        self.selector = None
        self.requires_matches = None

    def build(self, selector):
        self.selector = selector

        self.requires_matches = {}

        for key in self.selector.copy():
            if key in self.CAN_NOT_BUILD:
                self.requires_matches[key] = self.selector.pop(key)

        index = self.selector.pop('index', None)
        start_string = self.default_start
        adjacent_string = self._add_adjacent()
        tag_string = self._add_tag_name()
        class_string = self._add_class_predicates()
        attribute_string = self._add_attribute_predicates()
        converted_attribute_string = self._convert_attribute_predicates()
        text_string = self.add_text()

        xpath = ''.join((start_string, adjacent_string, tag_string, class_string, attribute_string,
                         converted_attribute_string, text_string))
        if index is not None:
            xpath = self._add_index(xpath, index, len(adjacent_string) > 0)

        self.selector.update(self.requires_matches)

        return {By.XPATH: xpath}

    def add_text(self):
        if 'text' not in self.selector:
            return ''

        text = self.selector.pop('text')
        if not isinstance(text, Pattern):
            return '[normalize-space()={}]'.format(XpathSupport.escape(text))
        else:
            self.requires_matches['text'] = text
            return ''

    @property
    def default_start(self):
        return './' if 'adjacent' in self.selector else './/*'

    @property
    def use_index(self):
        return True

    # private

    def _add_index(self, xpath, index=None, adjacent=None):
        if adjacent:
            return "{}[{}]".format(xpath, index + 1)
        elif index and index >= 0 and len(self.requires_matches) == 0 and self.use_index:
            return "({})[{}]".format(xpath, index + 1)
        elif index and index < 0 and len(self.requires_matches) == 0 and self.use_index:
            last_value = 'last()'
            if index < -1:
                last_value += str(index + 1)
            return "({})[{}]".format(xpath, last_value)
        else:
            self.requires_matches['index'] = index
            return xpath

    def _add_tag_name(self):
        tag_name = self.selector.pop('tag_name', None)

        if isinstance(tag_name, str):
            return "[local-name()='{}']".format(tag_name)
        if XpathSupport.is_simple_regexp(tag_name):
            return "[contains(local-name(), '{}')]".format(tag_name.pattern)
        elif tag_name is None:
            return ''
        else:
            self.requires_matches['tag_name'] = tag_name
            return ''

    def _add_attribute_predicates(self):
        element_attr_exp = self._attribute_expression
        if not element_attr_exp:
            return ''
        else:
            return '[{}]'.format(element_attr_exp)

    @property
    def _attribute_expression(self):
        expressions = []
        for key, value in self.selector.copy().items():
            if key == 'class' or key == 'text' or isinstance(value, Pattern):
                continue

            expressions.append(self._locator_expression(key, value))
            self.selector.pop(key)

        return ' and '.join([x for x in expressions if x is not None])

    def _equal_pair(self, key, value):
        if key == 'label_element':
            # we assume 'label' means a corresponding label element, not the attribute
            text = "normalize-space()={}".format(XpathSupport.escape(value))
            return "(@id=//label[{0}]/@for or parent::label[{0}])".format(text)
        else:
            return "{}={}".format(self._lhs_for(key), XpathSupport.escape(value))

    @staticmethod
    def _lhs_for(key):
        if key == 'href':
            return 'normalize-space(@href)'
        elif key == 'type':
            # type attributes can be upper case - downcase them
            # https://github.com/watir/watir/issues/72
            return XpathSupport.lower('@type')
        elif isinstance(key, str):
            if key.startswith('data') or key.startswith('aria'):
                return '@{}'.format(key.replace('_', '-'))
            else:
                return '@{}'.format(key)
        else:
            raise LocatorException('Unable to build XPath using {}:{}'.format(key, key.__class__))

    def _add_class_predicates(self):
        from nerodia.locators.class_helpers import ClassHelpers
        if 'class' not in self.selector:
            return ''

        self.requires_matches['class'] = []

        class_name = self.selector.pop('class', None)
        if isinstance(class_name, str) and ' ' in class_name.strip():
            self._deprecate_class_list(class_name)

        predicates = []
        if isinstance(class_name, bool):
            self.selector.pop('class')
            predicates = [self._locator_expression('class', class_name)]
        else:
            for x in ClassHelpers._flatten([class_name]):
                pred = self._class_predicate(x)
                if pred is not None:
                    predicates.append(pred)

        if len(self.requires_matches['class']) == 0:
            self.requires_matches.pop('class')

        if len(predicates) > 0:
            return '[{}]'.format(' and '.join(predicates))
        else:
            return ''

    def _deprecate_class_list(self, class_name):
        dep = "Using the 'class' locator to locate multiple classes with a String value " \
              "(i.e. '{}')".format(class_name)
        nerodia.logger.deprecate(dep, 'list (e.g. {})'.format(class_name.split()),
                                 ids=['class_list'])

    def _class_predicate(self, value):
        if isinstance(value, Pattern):
            predicate = self._convert_predicate('class', value)
            if predicate is None:
                self.requires_matches['class'].append(value)
            return predicate

        if re.search(r'^!', value):
            value = value[1:]
            negate_xpath = True
        else:
            negate_xpath = False

        xpath = "contains(concat(' ', @class, ' '), " \
                "{})".format(XpathSupport.escape(' {} '.format(value)))
        return "not({})".format(xpath) if negate_xpath else xpath

    def _locator_expression(self, key, val):
        if val is True:
            return self._attribute_presence(key)
        elif val is False:
            return self._attribute_absence(key)
        else:
            return self._equal_pair(key, val)

    def _add_adjacent(self):
        if 'adjacent' not in self.selector:
            return ''

        adjacent = self.selector.pop('adjacent')
        if adjacent == 'ancestor':
            return 'ancestor::*'
        elif adjacent == 'preceding':
            return 'preceding-sibling::*'
        elif adjacent == 'following':
            return 'following-sibling::*'
        elif adjacent == 'child':
            return 'child::*'
        else:
            raise LocatorException('Unable to process adjacent locator with {}'.format(adjacent))

    def _attribute_presence(self, attribute):
        return self._lhs_for(attribute)

    def _attribute_absence(self, attribute):
        return "not({})".format(self._lhs_for(attribute))

    def _convert_attribute_predicates(self):
        predicates = []
        for key in self.selector.copy():
            if key == 'text':
                continue

            predicate = self._convert_predicate(key, self.selector[key])
            self.selector.pop(key, None)
            predicates.append(predicate)

        return "[{}]".format(' and '.join(predicates)) if len(predicates) > 0 else ''

    def _convert_predicate(self, key, regexp):
        lhs = self._lhs_for(key)

        if XpathSupport.is_simple_regexp(regexp):
            return "contains({}, '{}')".format(lhs, regexp.pattern)
        elif key == 'class':
            self.requires_matches['class'].append(regexp)
        else:
            self.requires_matches[key] = regexp
        return lhs
