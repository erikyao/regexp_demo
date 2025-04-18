from abc import ABC, abstractmethod
from collections import deque


class State(ABC):
    def __init__(self):
        self.id = None

    @abstractmethod
    def transition_to(self, s: 'State'):
        pass


class LiteralState(State):
    def __init__(self, literal: str, next_state: State = None, _id=None):
        super().__init__()
        self.literal = literal
        self.next_state = next_state
        self.id = _id

    def transition_to(self, s: State):
        if self.next_state is None:
            self.next_state = s
            return 
        
        raise ValueError("Transition to {} already exists!".format(self.next_state))


class SplitState(State):
    def __init__(self, next_state_1: State = None, next_state_2: State = None, _id=None):
        super().__init__()
        self.next_state_1 = next_state_1
        self.next_state_2 = next_state_2
        self.id = _id

    def transition_to(self, s: State):
        if self.next_state_1 is None:
            self.next_state_1 = s
            return
        elif self.next_state_2 is None:
            self.next_state_2 = s
            return
        
        # (self.next_state_1 != None) & (self.next_state_2 != None)
        raise ValueError("Transitions to {} and {} already exist!".format(self.next_state_1, self.next_state_2))


class AcceptState(State):
    def __init__(self, _id=None):
        super().__init__()
        self.id = _id

    def transition_to(self, s: State):
        raise NotImplementedError("Should not call this function on an accept state!")


def assign_state_ids(start_state: State, start_id: int = 0):
    """
    Assigns an ID to each state in the NFA starting from `start_state`.
    ID is incremented naturally from `start_id`.
    """
    _id = start_id

    queue = deque([start_state])
    visited = set()
    while queue:  # BFS
        state = queue.popleft()
        
        if state in visited:
            continue

        visited.add(state)

        state.id = _id
        _id += 1

        if isinstance(state, LiteralState):
            queue.append(state.next_state)
        elif isinstance(state, SplitState):
            queue.append(state.next_state_1)
            queue.append(state.next_state_2)
        else:
            continue

    return


def nfa2str(start_state: State, assign_ids: bool = False, start_id: int = 0):
    output = []

    if assign_ids:
        assign_state_ids(start_state, start_id)
    
    queue = deque([start_state])
    visited = set()
    while queue:  # BFS
        state = queue.popleft()
        
        if state in visited:
            continue

        _id = state.id
        visited.add(state)

        if isinstance(state, LiteralState):
            next_id = state.next_state.id
            
            text = "[id:{:02d}][Lit] --- {} ---> [id:{:02d}]".format(_id, state.literal, next_id)
            output.append(text)

            queue.append(state.next_state)
        elif isinstance(state, SplitState):
            next_id_1 = state.next_state_1.id
            next_id_2 = state.next_state_2.id

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
