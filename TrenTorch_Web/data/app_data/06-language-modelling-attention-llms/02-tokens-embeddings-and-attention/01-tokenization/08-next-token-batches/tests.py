"""
pytest tests.py
"""

import numpy as np

from _load import load_solution

_module = load_solution(__file__)
make_lm_windows = _module.make_lm_windows


def test_1_hand_computed():
    X, Y = make_lm_windows(np.arange(7), block_size=3, stride=3)
    assert X.tolist() == [[0, 1, 2], [3, 4, 5]] and Y.tolist() == [[1, 2, 3], [4, 5, 6]]


def test_2_smaller_stride_overlaps():
    X, Y = make_lm_windows(np.arange(6), block_size=3, stride=1)
    assert X.tolist() == [[0, 1, 2], [1, 2, 3], [2, 3, 4]]
    assert Y.tolist() == [[1, 2, 3], [2, 3, 4], [3, 4, 5]]


def test_3_target_is_input_shifted_by_one():
    ids = np.random.RandomState(0).randint(0, 50, 100)
    X, Y = make_lm_windows(ids, 8, 4)
    assert np.array_equal(X[:, 1:], Y[:, :-1])


def test_4_number_of_windows_formula():
    for n, B, s in [(20, 4, 4), (21, 4, 4), (25, 5, 3)]:
        X, _ = make_lm_windows(np.arange(n), B, s)
        assert len(X) == (n - B - 1) // s + 1


def test_5_too_short_stream_gives_no_windows():
    X, Y = make_lm_windows(np.arange(3), 3, 1)
    assert X.shape == (0, 3) and Y.shape == (0, 3)


def test_6_last_target_never_reads_past_the_end():
    ids = np.arange(11)
    _, Y = make_lm_windows(ids, 5, 5)
    assert Y.max() <= 10


def test_7_independent_loop_oracle_and_input_untouched():
    ids = np.random.RandomState(1).randint(0, 9, 40)
    snap = ids.copy()
    X, Y = make_lm_windows(ids, 6, 5)
    w = 0
    s = 0
    while s + 7 <= 40:
        assert np.array_equal(X[w], ids[s:s + 6]) and np.array_equal(Y[w], ids[s + 1:s + 7])
        w += 1
        s += 5
    assert w == len(X) and np.array_equal(ids, snap)
