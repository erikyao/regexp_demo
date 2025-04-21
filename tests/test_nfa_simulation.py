import pytest

from src.re2post import re2post
from src.post2nfa import post2nfa
from src.nfa_simulation import match
from src.nfa_state import State


def compile_nfa(regex):
    postfix = re2post(regex)
    assert postfix is not None, f"Invalid regex: {regex}"
    start_state = post2nfa(postfix)
    assert start_state is not None, f"Failed to build NFA for: {postfix}"
    return start_state


@pytest.mark.parametrize("regex,string,expected", [
    # Basic matching
    ('a', 'a', True),
    ('a', 'b', False),
    ('ab', 'ab', True),
    ('ab', 'a', False),

    # Alternation
    ('a|b', 'a', True),
    ('a|b', 'b', True),
    ('a|b', 'c', False),
    ('ab|cd', 'ab', True),
    ('ab|cd', 'cd', True),

    # Quantifiers
    ('a*', '', True),
    ('a*', 'a', True),
    ('a*', 'aaaa', True),
    ('a+', '', False),
    ('a+', 'a', True),
    ('a?', '', True),
    ('a?', 'a', True),

    # Combined operations
    ('a*b|c+', 'b', True),
    ('a*b|c+', 'ab', True),
    ('a*b|c+', 'c', True),

    # Parentheses
    ('a(b|c)d', 'abd', True),
    ('a(b|c)d', 'acd', True),
    ('a(b|c)d', 'ad', False),

    # Edge cases
    ('', '', True),
    ('', 'a', False),
    ('(|)', '', True),
    ('(a*)*', 'aaa', True),
])
def test_nfa_matching(regex, string, expected):
    nfa = compile_nfa(regex)
    assert match(nfa, string) == expected


@pytest.mark.parametrize("regex", [
    'a',
    'a*',
    'a|b',
    'a(b|c)d'
])
def test_empty_string_handling(regex):
    nfa = compile_nfa(regex)
    with pytest.raises(ValueError):
        match(nfa, '')


def test_invalid_nfa():
    with pytest.raises(ValueError):
        match(None, 'abc')


@pytest.mark.parametrize("regex", [
    '*',  # Invalid: nothing to repeat
    '(',  # Unclosed paren
    'a|',  # Trailing |
    ')',  # Unmatched close
])
def test_invalid_regexes(regex):
    with pytest.raises((ValueError, AssertionError)):
        compile_nfa(regex)
