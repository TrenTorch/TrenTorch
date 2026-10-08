"""
pytest data/app_data/12-research-papers/02-transformers-and-llms/09-roformer/01-rope-frequencies/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-rope-frequencies")
rope_frequencies = _module.rope_frequencies


import numpy as np


def test_1_one_frequency_per_pair_of_features():
    assert rope_frequencies(8).shape == (4,)


def test_2_first_frequency_is_one():
    assert abs(rope_frequencies(6)[0] - 1.0) < 1e-12


def test_3_frequencies_decrease():
    f = rope_frequencies(10)
    assert np.all(np.diff(f) < 0)


def test_4_matches_a_hand_value_for_d_four():
    np.testing.assert_allclose(rope_frequencies(4), [1.0, 10000 ** -0.5])


def test_5_larger_base_gives_smaller_later_frequencies():
    assert rope_frequencies(4, base=100.0)[1] > rope_frequencies(4, base=10000.0)[1]


def test_6_returns_an_array():
    assert isinstance(rope_frequencies(4), np.ndarray)

