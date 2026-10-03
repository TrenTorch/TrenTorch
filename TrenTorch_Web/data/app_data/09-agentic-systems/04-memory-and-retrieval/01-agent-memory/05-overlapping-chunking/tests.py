"""
pytest tests.py
"""

from _load import load_solution

_module = load_solution(__file__)
chunk_tokens = _module.chunk_tokens


def test_1_hand_computed_with_overlap():
    assert chunk_tokens(list(range(10)), 4, 1) == [[0, 1, 2, 3], [3, 4, 5, 6], [6, 7, 8, 9]]


def test_2_no_overlap_is_a_plain_split():
    assert chunk_tokens(list(range(7)), 3, 0) == [[0, 1, 2], [3, 4, 5], [6]]


def test_3_shorter_than_one_chunk():
    assert chunk_tokens([1, 2], 5, 2) == [[1, 2]] and chunk_tokens([], 3, 1) == []


def test_4_last_chunk_that_reaches_the_end_stops_the_loop():
    # without the stop rule a final chunk [9] would repeat covered tokens
    assert chunk_tokens(list(range(10)), 4, 2) == [[0, 1, 2, 3], [2, 3, 4, 5], [4, 5, 6, 7], [6, 7, 8, 9]]


def test_5_every_token_is_covered():
    toks = list(range(53))
    covered = set(t for c in chunk_tokens(toks, 8, 3) for t in c)
    assert covered == set(toks)


def test_6_consecutive_chunks_share_exactly_the_overlap():
    chunks = chunk_tokens(list(range(40)), 10, 4)
    assert all(a[-4:] == b[:4] for a, b in zip(chunks, chunks[1:]))


def test_7_input_untouched_and_chunks_are_copies():
    toks = [1, 2, 3, 4, 5]
    out = chunk_tokens(toks, 3, 1)
    out[0][0] = 99
    assert toks == [1, 2, 3, 4, 5]
