"""
pytest data/app_data/12-research-papers/00-neural-network-foundations/02-he-initialization/02-he-init-sample/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-he-init-sample")
he_init_weights = _module.he_init_weights


import numpy as np


def test_1_shape_is_fan_out_by_fan_in():
    w = he_init_weights(4, 3, np.random.default_rng(0))
    assert w.shape == (3, 4)


def test_2_sample_std_is_close_to_he_rule():
    w = he_init_weights(100, 2000, np.random.default_rng(1))
    assert abs(w.std() - np.sqrt(2 / 100)) < 0.01


def test_3_sample_mean_is_close_to_zero():
    w = he_init_weights(100, 2000, np.random.default_rng(2))
    assert abs(w.mean()) < 0.01


def test_4_same_seed_same_weights():
    a = he_init_weights(5, 5, np.random.default_rng(9))
    b = he_init_weights(5, 5, np.random.default_rng(9))
    np.testing.assert_array_equal(a, b)


def test_5_different_seeds_give_different_weights():
    a = he_init_weights(5, 5, np.random.default_rng(1))
    b = he_init_weights(5, 5, np.random.default_rng(2))
    assert not np.array_equal(a, b)


def test_6_wider_fan_in_gives_smaller_entries():
    small = he_init_weights(10, 500, np.random.default_rng(3)).std()
    large = he_init_weights(1000, 500, np.random.default_rng(3)).std()
    assert large < small

