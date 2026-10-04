"""
pytest tests.py
"""

import numpy as np

from _load import load_solution

_module = load_solution(__file__)
solve_analogy = _module.solve_analogy
VOCAB = ["man", "woman", "king", "queen", "apple"]
# axes: [royalty, gender, fruit]
E = np.array([[0.0, 1.0, 0.0], [0.0, -1.0, 0.0], [1.0, 1.0, 0.0], [1.0, -1.0, 0.0], [0.0, 0.0, 1.0]])


def test_1_classic_analogy():
    assert solve_analogy(E, VOCAB, "man", "woman", "king") == "queen"


def test_2_reverse_direction():
    assert solve_analogy(E, VOCAB, "woman", "man", "queen") == "king"


def test_3_inputs_are_excluded_from_the_answer():
    # the target equals E[queen]; with queen excluded as an input the next best must differ
    out = solve_analogy(E, VOCAB, "man", "woman", "queen")
    assert out not in ("man", "woman", "queen")


def test_4_cosine_not_dot_product():
    E2 = E.copy()
    E2[3] *= 50.0
    assert solve_analogy(E2, VOCAB, "man", "woman", "king") == "queen"
    E3 = E.copy()
    E3[4] = [0.0, 0.0, 1000.0]
    assert solve_analogy(E3, VOCAB, "man", "woman", "king") == "queen"


def test_5_zero_vector_words_are_handled():
    E4 = np.vstack([E, np.zeros(3)])
    assert solve_analogy(E4, VOCAB + ["pad"], "man", "woman", "king") == "queen"


def test_6_lowest_index_wins_ties():
    E5 = np.array([[1.0, 0.0], [0.0, 1.0], [0.0, 0.0], [1.0, 1.0], [1.0, 1.0]])
    assert solve_analogy(E5, ["a", "b", "c", "d1", "d2"], "a", "b", "c") in ("d1", "d2")
    assert solve_analogy(E5, ["a", "b", "c", "d1", "d2"], "a", "b", "c") == "d1"


def test_7_inputs_untouched():
    snap, v = E.copy(), list(VOCAB)
    solve_analogy(E, VOCAB, "man", "woman", "king")
    assert np.array_equal(E, snap) and VOCAB == v
