# pytest test_re2post.py -v
#   -v flag gives verbose output so you can see which tests pass or fail

import pytest
from src.re2post import re2post

def test_basic_literals():
    assert re2post("a") == "a"
    assert re2post("ab") == "ab."
    assert re2post("abc") == "ab.c."

def test_alternation():
    assert re2post("a|b") == "ab|"
    assert re2post("a|b|c") == "abc||"
    assert re2post("ab|cd") == "ab.cd.|"

def test_repetition_operators():
    assert re2post("a*") == "a*"
    assert re2post("a+") == "a+"
    assert re2post("a?") == "a?"
    assert re2post("a*b+") == "a*b+."
    assert re2post("a|b*") == "ab*|"

def test_parentheses():
    assert re2post("(a)") == "a"
    assert re2post("(a|b)c") == "ab|c."
    assert re2post("a(b|c)") == "abc|."
    assert re2post("(ab)*") == "ab.*"
    assert re2post("(a|b)(c|d)") == "ab|cd|."

def test_complex_expressions():
    assert re2post("a(b|c)*d") == "abc|*.d."
    assert re2post("(a|b)*c(d|e)?") == "ab|*c.de|?."
    assert re2post("a+b?c*") == "a+b?.c*."

def test_edge_cases():
    assert re2post("") == ""
    assert re2post("((a))") == "a"
    assert re2post("(a|(b|c))") == "abc||"

def test_error_handling():
    with pytest.raises(ValueError):
        re2post("(a|)")  # Ends with alternation in parentheses

    with pytest.raises(ValueError):
        re2post("|a")  # Starts with alternation
    
    # with pytest.raises(ValueError):
    #     re2post("a|")  # Ends with alternation
    
    with pytest.raises(ValueError):
        re2post("(*)")  # No atom before *
    
    with pytest.raises(ValueError):
        re2post("(a")  # Unclosed parenthesis
    
    with pytest.raises(ValueError):
        re2post("a)")  # Unopened parenthesis

def test_implicit_concatenation():
    assert re2post("aa") == "aa."
    assert re2post("a(b)") == "ab."
    assert re2post("a*b") == "a*b."

def test_operator_priority():
    assert re2post("ab*") == "ab*."
    assert re2post("(ab)*") == "ab.*"
    assert re2post("a|b*") == "ab*|"
    assert re2post("(a|b)*") == "ab|*"