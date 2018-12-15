from re import IGNORECASE

from ..element.regexp_disassembler import RegexpDisassembler
from ..element.selector_builder import SelectorBuilder as ElementSelectorBuilder


class SelectorBuilder(ElementSelectorBuilder):
    # private

    def _build_wd_selector(self, selector):
        return self._build_link_text(selector) or self._build_partial_link_text(selector) or \
            super(SelectorBuilder, self)._build_wd_selector(selector)

    def _build_link_text(self, selector):
        if self._can_convert_to_link_text(selector):
            selector.pop('tag_name')
            return {'link_text': selector.pop('visible_text')}

    def _can_convert_to_link_text(self, selector):
        return set(selector) == {'tag_name', 'visible_text'} and \
            isinstance(selector.get('visible_text'), str)

    def _build_partial_link_text(self, selector):
        if self._convert_to_partial_link_text(selector):
            selector.pop('tag_name')
            return {'partial_link_text': selector.pop('visible_text').pattern}

    def _convert_to_partial_link_text(self, selector):
        regex = selector.get('visible_text')

        return set(selector) == {'tag_name', 'visible_text'} and not regex.flags & IGNORECASE and \
            RegexpDisassembler(regex).substrings[0] == regex.pattern
