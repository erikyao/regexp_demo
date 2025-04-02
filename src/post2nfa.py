from abc import ABC, abstractmethod
from collections import deque

class State(ABC):
    @abstractmethod
    def transition_to(self, s: 'State'):
        pass


class LiteralState(State):
    def __init__(self, literal: str, next_state: State = None):
        self.literal = literal
        self.next_state = next_state

    def transition_to(self, s: State):
        if self.next_state == None:
            self.next_state = s
            return 
        
        raise ValueError("Transition to {} already exists!".format(self.next_state))


class SplitState(State):
    def __init__(self, next_state_1: State = None, next_state_2: State = None):
        self.next_state_1 = next_state_1
        self.next_state_2 = next_state_2

    def transition_to(self, s: State):
        if self.next_state_1 == None:
            self.next_state_1 = s
            return
        elif self.next_state_2 == None:
            self.next_state_2 = s
            return
        
        # (self.next_state_1 != None) & (self.next_state_2 != None)
        raise ValueError("Transitions to {} and {} already exist!".format(self.next_state_1, self.next_state_2))


class AcceptState(State):
    def __init__(self):
        pass

    def transition_to(self, s: State):
        raise NotImplementedError("Should not call this function on an accept state!")


class Nfa:
    """
    A partially built NFA nfa without a accept state.
    - start: starting state of the nfa
    - ends: list of open States that need to be connected
    """
    def __init__(self, start: State, open_ends: list[State], accept: State = None):
        self.start = start
        self.open_ends = open_ends
        self.accept = accept

    def is_open(self):
        return self.open_ends and (self.accept == None)
    
    def is_closed(self):
        return not self.is_open()
        

def post2nfa(postfix: str):
    """
    Convert postfix regular expression to NFA using Thompson's construction algorithm.
    Returns the starting state of the NFA.
    
    The algorithm uses a stack to keep track of NFA nfas, combining them according to the operators in the postfix expression."
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


def assign_state_ids(start_state: State, start_id: int = 0):
    """
    Assigns an ID to each state in the NFA starting from `start_state`.
    ID is incremented naturally from `start_id`.
    Returns a map of {state : id}
    """

    id_map = dict()
    _id = start_id

    queue = deque([start_state])
    visited = set()
    while queue:  # BFS
        state = queue.popleft()
        
        if state in visited:
            continue

        visited.add(state)

        id_map[state] = _id
        _id += 1

        if isinstance(state, LiteralState):
            queue.append(state.next_state)
        elif isinstance(state, SplitState):
            queue.append(state.next_state_1)
            queue.append(state.next_state_2)
        else:
            continue

    return id_map


def nfa2str(start_state: State, start_id: int = 0):
    output = []

    id_map = assign_state_ids(start_state, start_id)
    
    queue = deque([start_state])
    visited = set()
    while queue:  # BFS
        state = queue.popleft()
        
        if state in visited:
            continue

        _id = id_map[state]
        visited.add(state)

        if isinstance(state, LiteralState):
            next_id = id_map[state.next_state]
            
            text = "[id:{:02d}][Lit] --- {} ---> [id:{:02d}]".format(_id, state.literal, next_id)
            output.append(text)

            queue.append(state.next_state)
        elif isinstance(state, SplitState):
            next_id_1 = id_map[state.next_state_1]
            next_id_2 = id_map[state.next_state_2]

            # '\u03B5' is the unicode for greek letter epsilon
            text_1 = "[id:{:02d}][Spl] --- {} ---> [id:{:02d}]".format(_id, u'\u03B5', next_id_1)
            # use `rjust` to align text_2 and text_1 to the right side
            text_2 = "`-- {} ---> [id:{:02d}]".format(u'\u03B5', next_id_2).rjust(len(text_1))
            
            output.append(text_1)
            output.append(text_2)

            queue.append(state.next_state_1)
            queue.append(state.next_state_2)
        else:
            text = "[id:{:02d}][Acc]".format(_id)
            output.append(text)

    return "\n".join(output)


if __name__ == "__main__":
    from re2post import re2post

    # assert re2post("a(b|c)*d") == "abc|*.d."
    # assert re2post("(a|b)*c(d|e)?") == "ab|*c.de|?."
    # assert re2post("a+b?c*") == "a+b?.c*."

    nfa = post2nfa(re2post("a(b|c)*d"))
    print(nfa2str(nfa), end="\n-----------\n")

    nfa = post2nfa(re2post("(a|b)*c(d|e)?"))
    print(nfa2str(nfa), end="\n-----------\n")

    nfa = post2nfa(re2post("a+b?c*"))
    print(nfa2str(nfa), end="\n-----------\n")