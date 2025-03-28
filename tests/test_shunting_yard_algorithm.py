# pytest test_shunting_yard_algorithm.py -v
#   -v flag gives verbose output so you can see which tests pass or fail

import pytest
from src.shunting_yard_algorithm import (
    is_operand, is_function_name, is_operator, 
    precedence, associativity, tokenize, sya
)

class TestHelperFunctions:
    def test_is_operand(self):
        assert is_operand('a') == True
        assert is_operand('z') == True
        assert is_operand('A') == False
        assert is_operand('1') == False
        assert is_operand('+') == False
        assert is_operand('ab') == False

    def test_is_function_name(self):
        assert is_function_name('A') == True
        assert is_function_name('Z') == True
        assert is_function_name('a') == False
        assert is_function_name('1') == False
        assert is_function_name('*') == False
        assert is_function_name('AB') == False

    def test_is_operator(self):
        assert is_operator('+') == True
        assert is_operator('-') == True
        assert is_operator('*') == True
        assert is_operator('/') == True
        assert is_operator('@') == True
        assert is_operator('#') == True
        assert is_operator('a') == False
        assert is_operator('A') == False
        assert is_operator('(') == False
        assert is_operator('++') == False

    def test_precedence(self):
        assert precedence('+') == 1
        assert precedence('-') == 1
        assert precedence('*') == 2
        assert precedence('/') == 2
        assert precedence('@') == 3
        assert precedence('#') == 3
        with pytest.raises(ValueError):
            precedence('(')
        with pytest.raises(ValueError):
            precedence('a')

    def test_associativity(self):
        assert associativity('+') == "LEFT"
        assert associativity('-') == "LEFT"
        assert associativity('*') == "LEFT"
        assert associativity('/') == "LEFT"
        assert associativity('@') == "RIGHT"
        assert associativity('#') == "RIGHT"
        with pytest.raises(ValueError):
            associativity('(')
        with pytest.raises(ValueError):
            associativity('a')

    def test_tokenize(self):
        assert list(tokenize("a + b")) == ['a', '+', 'b']
        assert list(tokenize("a+b")) == ['a', '+', 'b']
        assert list(tokenize("a + b * c")) == ['a', '+', 'b', '*', 'c']
        assert list(tokenize("a+(b*c)")) == ['a', '+', '(', 'b', '*', 'c', ')']
        assert list(tokenize("F(a, b)")) == ['F', '(', 'a', ',', 'b', ')']
        assert list(tokenize("a @ b # c")) == ['a', '@', 'b', '#', 'c']
        # Test with whitespace
        assert list(tokenize("  a  +  b  ")) == ['a', '+', 'b']


class TestShuntingYardAlgorithm:
    def test_simple_expressions(self):
        assert sya("a+b") == "ab+"
        assert sya("a-b") == "ab-"
        assert sya("a*b") == "ab*"
        assert sya("a/b") == "ab/"
        assert sya("a@b") == "ab@"
        assert sya("a#b") == "ab#"

    def test_precedence(self):
        assert sya("a+b*c") == "abc*+"
        assert sya("a*b+c") == "ab*c+"
        assert sya("a+b+c") == "ab+c+"
        assert sya("a*b*c") == "ab*c*"
        assert sya("a@b#c") == "abc#@"
        assert sya("a+b@c") == "abc@+"

    def test_parentheses(self):
        assert sya("(a+b)*c") == "ab+c*"
        assert sya("a*(b+c)") == "abc+*"
        assert sya("(a+b)*(c+d)") == "ab+cd+*"
        assert sya("((a+b)*c)+d") == "ab+c*d+"
        assert sya("a*(b*(c+d))") == "abcd+**"

    def test_functions(self):
        assert sya("F(a)") == "aF"
        assert sya("F(a,b)") == "abF"
        assert sya("F(a+b,c*d)") == "ab+cd*F"
        assert sya("F(G(a,b),c)") == "abGcF"
        assert sya("F(a,b)+c") == "abFc+"

    def test_complex_expressions(self):
        assert sya("a+b*(c-d)/e") == "abcd-*e/+"
        assert sya("a+b*c-(d/e+f*g)") == "abc*+de/fg*+-"
        assert sya("F(a+b,G(c,d*e))") == "ab+cde*GF"
        assert sya("(a@b)#(c+d*e)") == "ab@cde*+#"
        assert sya("a@b#c+d*e") == "abc#@de*+"

    def test_whitespace_handling(self):
        assert sya("a + b") == "ab+"
        assert sya("a +b* c") == "abc*+"
        assert sya(" a * ( b + c ) ") == "abc+*"
        assert sya("F ( a , b )") == "abF"

    def test_associativity(self):
        # Test left associativity of +, -, *, /
        assert sya("a+b+c") == "ab+c+"  # Should be (a+b)+c
        assert sya("a-b-c") == "ab-c-"  # Should be (a-b)-c
        assert sya("a*b*c") == "ab*c*"  # Should be (a*b)*c
        assert sya("a/b/c") == "ab/c/"  # Should be (a/b)/c
        
        # Test right associativity of @ and #
        assert sya("a@b@c") == "abc@@"  # Should be a@(b@c)
        assert sya("a#b#c") == "abc##"  # Should be a#(b#c)


class TestEdgeCases:
    def test_single_operand(self):
        assert sya("a") == "a"
    
    def test_nested_parentheses(self):
        assert sya("(((a)))") == "a"
        assert sya("(((a+b)))") == "ab+"
    
    def test_function_with_complex_args(self):
        assert sya("F((a+b)*(c-d), e@(f#g))") == "ab+cd-*efg#@F"
    
    def test_mixed_operators_and_functions(self):
        assert sya("F(a,b) + G(c,d) * H(e,f)") == "abFcdGefH*+"