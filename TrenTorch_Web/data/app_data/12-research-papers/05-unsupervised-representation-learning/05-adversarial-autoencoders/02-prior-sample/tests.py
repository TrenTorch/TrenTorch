"""
pytest data/app_data/12-research-papers/05-unsupervised-and-representation-learning/05-adversarial-autoencoders/02-prior-sample/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-aae-prior-sample")
prior_sample = _module.prior_sample


import numpy as np


def test_1_output_shape():
    assert prior_sample(np.random.default_rng(0), 5, 3).shape == (5, 3)


def test_2_same_seed_gives_same_samples():
    a = prior_sample(np.random.default_rng(4), 4, 2)
    b = prior_sample(np.random.default_rng(4), 4, 2)
    np.testing.assert_array_equal(a, b)


def test_3_large_sample_has_mean_near_zero():
    x = prior_sample(np.random.default_rng(1), 20000, 2)
    np.testing.assert_allclose(x.mean(axis=0), 0.0, atol=0.05)


def test_4_large_sample_has_unit_variance():
    x = prior_sample(np.random.default_rng(2), 20000, 2)
    np.testing.assert_allclose(x.var(axis=0), 1.0, atol=0.05)


def test_5_returns_floats():
    assert prior_sample(np.random.default_rng(0), 2, 2).dtype.kind == "f"


def test_6_different_seeds_differ():
    a = prior_sample(np.random.default_rng(1), 3, 3)
    b = prior_sample(np.random.default_rng(2), 3, 3)
    assert not np.array_equal(a, b)

