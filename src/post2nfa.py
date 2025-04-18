from .nfa import SplitState, LiteralState, AcceptState, Nfa, State


def post2nfa(postfix: str | None) -> State | None:
    """
    Convert postfix regular expression to NFA using Thompson's construction algorithm.
    Returns the starting state of the NFA.
    
    The algorithm uses a stack to keep track of NFAs, combining them according to the operators in the postfix expression."
    """

    if postfix is None:
        return None
    
    component_stack = []

    for c in postfix:
        if c == '.':  # Concatenation
            # Pop out two open NFAs and connect them
            nfa2 = component_stack.pop()
            nfa1 = component_stack.pop()
            
            # Connect all open ends from nfa1 to start of nfa2
            for end_state in nfa1.open_ends:
                end_state.transition_to(nfa2.start)
            nfa1.open_ends = nfa2.open_ends

            component_stack.append(nfa1)

        elif c == '|':  # Alternation
            # Pop out two open NFAs and create a new SPLIT state
            nfa2 = component_stack.pop()
            nfa1 = component_stack.pop()
            
            # Create a new state that splits to both :02d
            s = SplitState(nfa1.start, nfa2.start)
            
            # Combine the open ends from both NFAs
            new_nfa = Nfa(s, nfa1.open_ends + nfa2.open_ends)
            component_stack.append(new_nfa)

        elif c == '?':  # Zero or one
            # Pop out one open Nfa and make it optional
            nfa = component_stack.pop()
            
            # Create a SPLIT state that can skip the nfa
            s = SplitState(nfa.start, None)

            # Combine nfa's ends with the new skip path
            new_nfa = Nfa(s, nfa.open_ends + [s])  # s is an open end because s.next_state_2 is None
            component_stack.append(new_nfa)

        elif c == '*':  # Zero or more
            # Pop out one open Nfa and make it repeatable
            nfa = component_stack.pop()
            
            # Create a SPLIT state that loops back
            s = SplitState(nfa.start, None)
            
            # Connect all open ends to the SPLIT state to create loop
            for end_state in nfa.open_ends:
                end_state.transition_to(s)
            
            # The new nfa can skip or loop
            new_nfa = Nfa(s, [s])  # s is an open end because s.next_state_2 is None
            component_stack.append(new_nfa)  

        elif c == '+':  # One or more
            # Pop one open Nfa and make it repeatable (but must match at least once)
            nfa = component_stack.pop()
            
            # Create a SPLIT state that loops back
            s = SplitState(nfa.start, None)
            
            # Connect all open ends to the SPLIT state to create loop
            for end_state in nfa.open_ends:
                end_state.transition_to(s)
            nfa.open_ends = [s]  # s is an open end because s.next_state_2 is None

            component_stack.append(nfa)  
            
        else:  # Literal character
            # Create a state that transitions on this character
            s = LiteralState(c, None)
            
            # The nfa is just this state with one open end
            new_nfa = Nfa(s, [s])
            component_stack.append(new_nfa)

    # After processing all characters, we should have exactly one nfa left
    if len(component_stack) != 1:
        return None  # Invalid postfix expression
    
    final_nfa = component_stack[0]
    assert final_nfa.is_open()

    accept_state = AcceptState()
    for end_state in final_nfa.open_ends:
        end_state.transition_to(accept_state)
    final_nfa.open_ends = []
    final_nfa.accept = accept_state
    
    assert final_nfa.is_closed()

    return final_nfa.start
