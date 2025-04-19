import pytest

from src.nfa_state import (SplitState, LiteralState, AcceptState, epsilon_closure, epsilon_closure_recursive,
                           assign_state_ids)
from src.post2nfa import post2nfa


@pytest.fixture
def setup_simple_nfa():
    return {
        'one_char': post2nfa('a'),
        'one_concat': post2nfa('ab.'),
        'one_alternate': post2nfa('ab|'),
        'one_star': post2nfa('a*'),
        'one_plus': post2nfa('a+'),
        'one_question': post2nfa('a?')
    }


@pytest.fixture
def setup_loop_nfa():
    start = SplitState()
    s1 = SplitState()
    s2 = LiteralState('a')
    accept = AcceptState()

    start.next_state_1 = s1
    start.next_state_2 = s1
    s1.next_state_1 = start
    s1.next_state_2 = s2
    s2.next_state = accept

    return start


def test_assign_state_ids(setup_simple_nfa):
    start_state = setup_simple_nfa['one_char']
    assign_state_ids(start_state)
    assert start_state.id == 0
    assert start_state.next_state.id == 1

    start_state = setup_simple_nfa['one_concat']
    assign_state_ids(start_state, 1)
    assert start_state.id == 1
    assert start_state.next_state.id == 2
    assert start_state.next_state.next_state.id == 3

    start_state = setup_simple_nfa['one_alternate']
    assign_state_ids(start_state, 1)
    assert start_state.id == 1
    assert start_state.next_state_1.id == 2
    assert start_state.next_state_2.id == 3
    assert start_state.next_state_1.next_state.id == 4
    assert start_state.next_state_2.next_state.id == 4

    start_state = setup_simple_nfa['one_star']
    assign_state_ids(start_state, 1)
    assert start_state.id == 1
    assert start_state.next_state_1.id == 2
    assert start_state.next_state_2.id == 3
    assert start_state.next_state_1.next_state.id == 1

    start_state = setup_simple_nfa['one_plus']
    assign_state_ids(start_state, 1)
    assert start_state.id == 1
    assert start_state.next_state.id == 2
    assert start_state.next_state.next_state_1.id == 1
    assert start_state.next_state.next_state_2.id == 3

    start_state = setup_simple_nfa['one_question']
    assign_state_ids(start_state, 1)
    assert start_state.id == 1
    assert start_state.next_state_1.id == 2
    assert start_state.next_state_2.id == 3
    assert start_state.next_state_1.next_state.id == 3


def test_epsilon_closure(setup_simple_nfa):
    assert epsilon_closure([]) is None

    start_state = setup_simple_nfa['one_char']
    closure = epsilon_closure([start_state])
    assert len(closure) == 1
    assert start_state in closure

    start_state = setup_simple_nfa['one_concat']
    closure = epsilon_closure([start_state, start_state.next_state])
    assert len(closure) == 2
    assert start_state in closure
    assert start_state.next_state in closure

    start_state = setup_simple_nfa['one_alternate']
    closure = epsilon_closure([start_state])
    assert len(closure) == 3
    assert start_state in closure
    assert start_state.next_state_1 in closure
    assert start_state.next_state_2 in closure

    start_state = setup_simple_nfa['one_star']
    closure = epsilon_closure([start_state])
    assert len(closure) == 3
    assert start_state in closure
    assert start_state.next_state_1 in closure
    assert start_state.next_state_2 in closure

    start_state = setup_simple_nfa['one_plus']
    closure = epsilon_closure([start_state, start_state.next_state])
    assert len(closure) == 3
    assert start_state in closure
    assert start_state.next_state.next_state_1 in closure
    assert start_state.next_state.next_state_2 in closure

    start_state = setup_simple_nfa['one_question']
    closure = epsilon_closure([start_state])
    assert len(closure) == 3
    assert start_state in closure
    assert start_state.next_state_1 in closure
    assert start_state.next_state_2 in closure


def test_epsilon_closure_with_loop(setup_loop_nfa):
    start_state = setup_loop_nfa
    closure = epsilon_closure([start_state])
    assert len(closure) == 3
    assert start_state in closure
    assert start_state.next_state_1 in closure
    assert start_state.next_state_2 is start_state.next_state_1
    assert start_state.next_state_1.next_state_1 in closure


def test_epsilon_closure_recursive(setup_simple_nfa):
    assert epsilon_closure_recursive([]) is None

    start_state = setup_simple_nfa['one_char']
    closure_1 = epsilon_closure([start_state])
    closure_2 = epsilon_closure_recursive([start_state])
    assert closure_1 == closure_2

    start_state = setup_simple_nfa['one_concat']
    closure_1 = epsilon_closure([start_state, start_state.next_state])
    closure_2 = epsilon_closure_recursive([start_state, start_state.next_state])
    assert closure_1 == closure_2

    start_state = setup_simple_nfa['one_alternate']
    closure_1 = epsilon_closure([start_state])
    closure_2 = epsilon_closure_recursive([start_state])
    assert closure_1 == closure_2

    start_state = setup_simple_nfa['one_star']
    closure_1 = epsilon_closure([start_state])
    closure_2 = epsilon_closure_recursive([start_state])
    assert closure_1 == closure_2

    start_state = setup_simple_nfa['one_plus']
    closure_1 = epsilon_closure([start_state, start_state.next_state])
    closure_2 = epsilon_closure_recursive([start_state, start_state.next_state])
    assert closure_1 == closure_2

    start_state = setup_simple_nfa['one_question']
    closure_1 = epsilon_closure([start_state])
    closure_2 = epsilon_closure_recursive([start_state])
    assert closure_1 == closure_2


def test_epsilon_closure_recursive_with_loop(setup_loop_nfa):
    start_state = setup_loop_nfa
    closure_1 = epsilon_closure([start_state])
    closure_2 = epsilon_closure_recursive([start_state])
    assert closure_1 == closure_2
