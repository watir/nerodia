from ..element.matcher import Matcher as ElementMatcher


class Matcher(ElementMatcher):
    # private

    def _elements_match(self, element, values_to_match):
        tag_name = self._fetch_value(element, 'tag_name')
        if tag_name == 'input':
            for key in ('text', 'label', 'visible_text'):
                if key in values_to_match:
                    values_to_match['value'] = values_to_match.pop(key)
        elif tag_name == 'label':
            for key in ('value', 'label'):
                if key in values_to_match:
                    values_to_match['text'] = values_to_match.pop(key)
        else:
            return None

        return super(Matcher, self)._elements_match(element, values_to_match)

    def _text_regexp_deprecation(self, *args):
        return None  # does not apply to text_field

    def _validate_tag(self, element, _expected):
        return self._matches_values(self._fetch_value(element, 'tag_name'), 'input')
