from src.post2nfa import post2nfa
from src.nfa_state import LiteralState, AcceptState, SplitState

# import pytest
# @pytest.fixture
# def basic_nfa():
#     """Fixture providing simple NFAs for testing"""
#     def one_char_nfa():
#         start = LiteralState('a')
#         accept = AcceptState()
#         start.next_state = accept
#         return start
#
#     def one_concat_nfa():
#         start = LiteralState('a')
#         second = LiteralState('b')
#         accept = AcceptState()
#
#         start.next_state = second
#         second.next_state = accept
#         return start
#
#     def one_alternate_nfa():
#         start = SplitState()
#         b1 = LiteralState('a')
#         b2 = LiteralState('b')
#         accept = AcceptState()
#
#         start.next_state_1 = b1
#         start.next_state_2 = b2
#         b1.next_state = accept
#         b2.next_state = accept
#
#         return start
#
#     def one_star_nfa():
#         start = SplitState()
#         b1 = LiteralState('a')
#         accept = AcceptState()
#
#         start.next_state_1 = b1
#         start.next_state_2 = accept
#         b1.next_state = start
#
#         return start
#
#     def one_plus_nfa():
#         start = LiteralState('a')
#         split = SplitState()
#         accept = AcceptState()
#
#         start.next_state = split
#         split.next_state_1 = start
#         split.next_state_2 = accept
#
#         return start
#
#     def one_question_nfa():
#         start = SplitState()
#         b1 = LiteralState('a')
#         accept = AcceptState()
#
#         start.next_state_1 = b1
#         start.next_state_2 = accept
#         b1.next_state = accept
#
#         return start
#
#     return {
#         'one_char': ('a', one_char_nfa()),
#         'one_concat': ('ab.', one_concat_nfa()),
#         'one_alternate': ('ab|', one_alternate_nfa()),
#         'star': ('a*', one_star_nfa()),
#         'plus': ('a+', one_plus_nfa()),
#         'question': ('a?', one_question_nfa())
#     }


def test_post2nfa_one_char():
    postfix = 'a'
    start = post2nfa(postfix)

    assert start is not None
    assert isinstance(start, LiteralState)
    assert start.literal == 'a'

    assert start.next_state is not None
    assert isinstance(start.next_state, AcceptState)


def test_post2nfa_one_concat():
    postfix = 'ab.'
    start = post2nfa(postfix)

    assert start is not None
    assert isinstance(start, LiteralState)
    assert start.literal == 'a'

    assert start.next_state is not None
    assert isinstance(start.next_state, LiteralState)
    assert start.next_state.literal == 'b'

    assert start.next_state.next_state is not None
    assert isinstance(start.next_state.next_state, AcceptState)


def one_alternate():
    postfix = 'ab|'
    start = post2nfa(postfix)

    assert start is not None
    assert isinstance(start, LiteralState)
    assert start.literal == 'a'

    assert start.next_state is not None
    assert isinstance(start.next_state, LiteralState)
    assert start.next_state.literal == 'b'

    assert start.next_state.next_state is not None
    assert isinstance(start.next_state.next_state, AcceptState)


def test_one_star():
    postfix = 'a*'
    start = post2nfa(postfix)

    assert start is not None
    assert isinstance(start, SplitState)

    assert start.next_state_1 is not None
    assert isinstance(start.next_state_1, LiteralState)
    assert start.next_state_1.literal == 'a'

    assert start.next_state_2 is not None
    assert isinstance(start.next_state_2, AcceptState)

    assert start.next_state_1.next_state is start


def test_one_plus():
    postfix = 'a+'
    start = post2nfa(postfix)

    assert start is not None
    assert isinstance(start, LiteralState)
    assert start.literal == 'a'

    assert start.next_state is not None
    assert isinstance(start.next_state, SplitState)

    assert start.next_state.next_state_1 is start

    assert start.next_state.next_state_2 is not None
    assert isinstance(start.next_state.next_state_2, AcceptState)


def test_one_question():
    postfix = 'a?'
    start = post2nfa(postfix)

    assert start is not None
    assert isinstance(start, SplitState)

    assert start.next_state_1 is not None
    assert isinstance(start.next_state_1, LiteralState)
    assert start.next_state_1.literal == 'a'

    assert start.next_state_2 is not None
    assert isinstance(start.next_state_2, AcceptState)

    assert start.next_state_1.next_state is start.next_state_2


def test_post2nfa_invalid_input():
    """Test error handling for invalid postfix expressions"""
    assert post2nfa(None) is None
    assert post2nfa('') is None
    assert post2nfa('a*b') is None  # Invalid postfix
    # assert post2nfa('a.b') is None  # Invalid postfix  # TODO add exception handling
    assert post2nfa('(ab)') is None  # Infix not supported


# TODO test complex cases
# def test_post2nfa_complex_expressions():
#     """Test more complex expressions"""
#     # a(b|c)*
#     nfa = post2nfa('abc|*.')
#     assert nfa is not None
#     states = collect_states(nfa)
#     assert len(states) == 6  # Verify correct state count
#
#     # (ab)*|c+
#     nfa = post2nfa('ab.*c+|')
#     assert nfa is not None
#     states = collect_states(nfa)
#     assert len(states) == 7
