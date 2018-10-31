# Translated to python from https://github.com/teamcapybara/capybara/blob/663a6003c0fa45fb83c55593183fdb2542a845ba/lib/capybara/selector/regexp_disassembler.rb

import re
from collections import OrderedDict


class RegexpDisassembler(object):

    COUNTED_REP_REGEX = r'(?P<char>.)\{(?P<min_rep>\d*)(?:,(?P<max_rep>\d*))?\}(?P<min>\?)?'
    GROUP_REGEX = r'(?P<group>\([^()]*\))' \
                  r'(?:' \
                  r'(?:' \
                  r'(?P<optional>[*?]) |' \
                  r'(?P<one_or_more>\+) |' \
                  r'(?:{})' \
                  r')\??' \
                  r')?'.format(COUNTED_REP_REGEX)

    def __init__(self, regexp):
        self.regexp = regexp
        self.pattern = self.regexp.pattern
        self._substrings = None

    @property
    def substrings(self):
        if self._substrings is not None:
            return self._substrings

        strs = []
        pattern = self.pattern
        # replace escaped characters and numbered back references with wildcard
        pattern = re.sub(r'\\.', '.', pattern)
        # replace named backreferences with wildcard
        pattern = re.sub(r'\(\?P=[^)]+\)', '.', pattern)
        # replace character classes with wildcard
        prev = ''
        while prev != pattern:
            prev = pattern
            pattern = re.sub(r'\(\?<?[=!][^)]*\)', '.', pattern)
        # remove lookahead/lookbehind assertions
        pattern = re.sub(r'\(\?<?[=!][^)]*\)', '', pattern)
        # replace named and non-matching groups with unnamed matching groups
        pattern = re.sub(r'\(\?P?(?:<[^>]+>|:)', '(', pattern)

        # simplify groups
        prev = ''
        while prev != pattern:
            prev = pattern
            pattern = re.sub(RegexpDisassembler.GROUP_REGEX,
                             lambda x: self._simplify_group(x),
                             pattern)

        # replace optional character with wildcard
        pattern = re.sub(r'.[*?]\??', '.', pattern)
        # replace one or more with character plus wildcard
        pattern = re.sub(r'(.)\+\??', r'\1.', pattern)
        # repeat counted characters
        match = re.search(RegexpDisassembler.COUNTED_REP_REGEX, pattern)
        if match is not None:
            final = match.group('char') * int(match.group('min_rep'))
            if match.group('max_rep') is not None and match.group('min') is None:
                final += '.'
            pattern = re.sub(RegexpDisassembler.COUNTED_REP_REGEX, final, pattern)

        if '|' in pattern:  # can't handle alternation here
            return []
        match = re.search(r'\A\^?(.*?)\$?\Z', pattern)
        if match is not None:
            strs = list(OrderedDict.fromkeys(x for x in match.group(1).split('.') if len(x) > 0))
            if self.regexp.flags & re.IGNORECASE:
                strs = [x.lower() for x in strs]
        return strs

    @staticmethod
    def _simplify_group(match):  # no support for alternation in groups
        if '|' in match.group('group') is not None:
            return '.'
        elif match.group('one_or_more') is not None:  # required but may repeat becomes text + wildcard
            return match.group('group')[1:-1] + '.'
        elif match.group('optional') is not None:
            return '.'
        elif match.group('min_rep') is not None:
            str = match.group('group') * int(match.group('min_rep'))
            if match.group('max_rep') is not None:
                str += '.'
            return str
        else:
            return match.group('group')[1:-1]
