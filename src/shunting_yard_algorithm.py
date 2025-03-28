from collections import deque
import re

PLUS_MINUS_OPS = "+-"
MUL_DIV_OPS = "*/"
VIRTUAL_OPS = "@#"  # some imaginary operators just for the purpose of demostration
BIN_OPS = PLUS_MINUS_OPS + MUL_DIV_OPS + VIRTUAL_OPS

def is_operand(token: str):
    return len(token) == 1 and token.islower()

def is_function_name(token: str):
    return len(token) == 1 and token.isupper()

def is_operator(token: str):
    return len(token) == 1 and token in BIN_OPS

def precedence(op):
    if op in PLUS_MINUS_OPS:
        return 1
    elif op in MUL_DIV_OPS:
        return 2
    elif op in VIRTUAL_OPS:
        return 3
    
    raise ValueError("Cannot recognize op " + op)

def associativity(op):
    if op in PLUS_MINUS_OPS or op in MUL_DIV_OPS:
        return "LEFT"
    elif op in VIRTUAL_OPS:
        return "RIGHT"
    
    raise ValueError("Cannot recognize op " + op)

def tokenize(input: str):
    # remove all whitespaces
    ret = ''.join(input.split())

    # [] indicates a character class
    # Outmost () indicates "capturing"; when used, the delimeters are also returned in the output
    ret = re.split("([{}])".format(re.escape("()," + BIN_OPS)), ret)

    # get rid of the possible tailing empty string after re.split()
    return filter(None, ret)

def sya(input: str):
    output_queue = deque()
    operator_stack = list()

    for token in tokenize(input):
        if is_operand(token):
            output_queue.append(token)
        elif is_function_name(token):
            operator_stack.append(token)
        elif token == ",":  # as in "f(a,b)"
            """
            E.g. input == "f(a,b)": 扫描到 "," 时, stack = ["f", "("], queue = ["a"], 此时 do nothing
            E.g. input == "f(a+b, c)": 扫描到 "," 时, stack = ["f", "(", "+"], queue = ["a", "b"], 此时把 "+" 从 stack 中弹出，并压入 queue
            """
            while operator_stack and operator_stack[-1] != '(':
                op = operator_stack.pop()
                output_queue.append(op)
        elif is_operator(token):
            op1 = token
            """
            For input like "a op2 b op1 c"
            """
            while operator_stack and operator_stack[-1] != '(':
                op2 = operator_stack[-1]

                if precedence(op2) > precedence(op1) or (precedence(op2) == precedence(op1) and associativity(op1) == "LEFT"):
                    operator_stack.pop()  # i.e. pop out op2
                    output_queue.append(op2)
                else:
                    break
            operator_stack.append(op1)
        elif token == "(":
            operator_stack.append(token)
        elif token == ")":
            while operator_stack and operator_stack[-1] != '(':
                op = operator_stack.pop()
                output_queue.append(op)

            # otherwise there are mismatched parentheses.
            assert(operator_stack)
            assert(operator_stack[-1] == '(') 

            operator_stack.pop()  # just discard the left paren

            if operator_stack and is_function_name(operator_stack[-1]):
                f_name = operator_stack.pop()
                output_queue.append(f_name)

    while operator_stack:
        assert(operator_stack[-1] != "(")  # otherwise there are mismatched parentheses.
        op = operator_stack.pop()
        output_queue.append(op)

    return "".join(output_queue)
