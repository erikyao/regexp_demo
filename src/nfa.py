from abc import ABC, abstractmethod

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
