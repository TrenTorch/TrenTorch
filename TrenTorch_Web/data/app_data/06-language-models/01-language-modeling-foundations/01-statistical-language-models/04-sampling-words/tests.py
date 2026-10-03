"""
pytest tests.py
"""

import numpy as np

from _load import load_solution

_module = load_solution(__file__)
sample_word = _module.sample_word

ITOS = [".", "a", "b"]


def test_1_deterministic_chain():
    probs = np.array([[0, 1.0, 0], [0, 0, 1.0], [1.0, 0, 0]])
    assert sample_word(probs, ITOS, np.random.RandomState(0)) == "ab"


def test_2_hand_computed_draws():
    class FixedRng:
        def __init__(self, values):
            self.values = list(values)

        def random_sample(self):
            return self.values.pop(0)

    probs = np.array([[0.0, 0.5, 0.5], [0.5, 0.25, 0.25], [0.25, 0.5, 0.25]])
    # row 0 cum [0, .5, 1]: u=0.7 -> b ; row b cum [.25,.75,1]: u=0.3 -> a ;
    # row a cum [.5,.75,1]: u=0.1 -> boundary
    assert sample_word(probs, ITOS, FixedRng([0.7, 0.3, 0.1])) == "ba"


def test_3_max_len_truncates():
    probs = np.array([[0, 1.0, 0], [0, 1.0, 0], [0, 1.0, 0]])
    assert sample_word(probs, ITOS, np.random.RandomState(0), max_len=4) == "aaaa"


def test_4_matches_independent_replay_of_the_same_seed():
    rng_probs = np.random.RandomState(7)
    raw = rng_probs.rand(4, 4) + 0.05
    probs = raw / raw.sum(axis=1, keepdims=True)
    itos = [".", "x", "y", "z"]
    for seed in range(5):
        got = sample_word(probs, itos, np.random.RandomState(seed))
        r = np.random.RandomState(seed)
        state, chars = 0, []
        for _ in range(50):
            u = r.random_sample()
            cum = np.cumsum(probs[state])
            j = next((k for k in range(4) if cum[k] > u), 3)
            if j == 0:
                break
            chars.append(itos[j])
            state = j
        assert got == "".join(chars)


def test_5_empirical_frequencies_follow_the_row():
    probs = np.array([[0.0, 0.8, 0.2], [1.0, 0, 0], [1.0, 0, 0]])
    rng = np.random.RandomState(0)
    words = [sample_word(probs, ITOS, rng) for _ in range(2000)]
    assert abs(words.count("a") / 2000 - 0.8) < 0.04


def test_6_probs_not_modified():
    probs = np.array([[0, 1.0, 0], [0, 0, 1.0], [1.0, 0, 0]])
    snapshot = probs.copy()
    sample_word(probs, ITOS, np.random.RandomState(0))
    assert np.array_equal(probs, snapshot)
