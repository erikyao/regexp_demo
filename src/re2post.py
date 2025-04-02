from collections import deque

# def precedence(op):
#     """Helper function to determine operator precedence."""
#     if op in ('|', '.'):
#         return 1
#     if op in ('*', '+', '?'):
#         return 2
#     return 0


# def associativity(op):
#     """Helper function to determine operator associativity."""
#     if op == '|':
#         return "RIGHT"
#     return "LEFT"


def re2post(regex):
    """
    Convert infix regular expression to postfix notation.
    Insert '.' as explicit concatenation operator.
    """
    output_queue = deque()  # Output queue for postfix expression
    operator_stack = []    # Stack for operators and parentheses
    n_alt_ops = 0      # Number of seen alternation operators (i.e. '|')
    n_con_opnds = 0     # Number of seen atoms (if n_atoms >= 2, it's time to insert the concatenation operator '.')

    def check_and_insert_one_dot():
        nonlocal n_con_opnds, output_queue
        if n_con_opnds >= 2:
            n_con_opnds -= 1
            output_queue.append('.')

    def check_and_insert_all_dots():
        nonlocal n_con_opnds, output_queue
        while (n_con_opnds := n_con_opnds - 1) >= 1:
            output_queue.append('.')

    def check_and_insert_all_bars():
        nonlocal n_alt_ops, output_queue
        if n_alt_ops >= 1:
            output_queue.append('|' * n_alt_ops)

    for c in regex:
        if c == '(':
            check_and_insert_one_dot()

            # store the old stats
            operator_stack.append((n_alt_ops, n_con_opnds))
            
            # init new stats for inside-parentheses expression
            n_alt_ops = 0
            n_con_opnds = 0
        elif c == '|':
            if n_con_opnds == 0:
                raise ValueError("Invalid regular expression")
            
            check_and_insert_all_dots()
            assert n_con_opnds == 0

            n_alt_ops += 1
        elif c == ')':
            if not operator_stack:
                raise ValueError("Invalid regular expression")
            if n_con_opnds == 0:
                raise ValueError("Invalid regular expression")
            
            check_and_insert_all_dots()
            check_and_insert_all_bars()
            assert n_con_opnds == 0
            # no need to reset n_con_opnds or n_alt_ops since we are going to laod the old values
            
            n_alt_ops, n_con_opnds = operator_stack.pop()  # load the old stats when '(' is scanned 
            n_con_opnds += 1
        elif c in ('*', '+', '?'):
            if n_con_opnds == 0:
                raise ValueError("Invalid regular expression")
            output_queue.append(c)
        else:
            check_and_insert_one_dot()

            output_queue.append(c)
            n_con_opnds += 1

    if operator_stack:
        raise ValueError("Invalid regular expression")

    check_and_insert_all_dots()
    check_and_insert_all_bars()
    # no need to reset n_con_opnds or n_alt_ops in the end

    return ''.join(output_queue)
