"""
pytest data/app_data/12-research-papers/09-sequence-models-and-attention/04-show-attend-tell/03-hard-attention-sample/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-sat-hard-sample")
sample_hard_attention = _module.sample_hard_attention


import numpy as np


def test_1_one_hot_samples_that_location():
    assert sample_hard_attention(np.array([0.0, 1.0, 0.0]), np.random.default_rng(0)) == 1


def test_2_same_seed_same_sample():
    a = sample_hard_attention(np.array([0.2, 0.8]), np.random.default_rng(3))
    b = sample_hard_attention(np.array([0.2, 0.8]), np.random.default_rng(3))
    assert a == b


def test_3_returns_a_python_int():
    assert isinstance(sample_hard_attention(np.array([1.0]), np.random.default_rng(0)), int)


def test_4_sample_is_a_valid_index():
    s = sample_hard_attention(np.array([0.3, 0.3, 0.4]), np.random.default_rng(5))
    assert 0 <= s < 3


def test_5_frequencies_follow_the_distribution():
    rng = np.random.default_rng(1)
    draws = [sample_hard_attention(np.array([0.1, 0.9]), rng) for _ in range(2000)]
    assert abs(np.mean(draws) - 0.9) < 0.05


def test_6_does_not_mutate_alpha():
    a = np.array([0.5, 0.5])
    sample_hard_attention(a, np.random.default_rng(0))
    np.testing.assert_array_equal(a, [0.5, 0.5])

