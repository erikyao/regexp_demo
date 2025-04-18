from collections import deque

from src.nfa_state import State, LiteralState, SplitState, AcceptState, assign_state_ids


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
        elif isinstance(state, AcceptState):
            text = "[id:{:02d}][Acc]".format(_id)
            output.append(text)
        else:
            raise ValueError("Cannot recognize State class!")

    return "\n".join(output)
