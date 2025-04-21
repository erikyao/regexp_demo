from src.nfa_state import State, LiteralState, AcceptState, epsilon_closure


def match(start_state: State, _input: str) -> bool:
    if start_state is None:
        raise ValueError("Invalid NFA!")

    if not _input:
        raise ValueError("Invalid input!")

    current_closure = epsilon_closure(start_state)
    for c in _input:
        valid_states = [s for s in current_closure if isinstance(s, LiteralState) and s.literal == c]
        current_closure = epsilon_closure(valid_states)
        if current_closure is None:
            return False

    for s in current_closure:
        if isinstance(s, AcceptState):
            return True

    return False
