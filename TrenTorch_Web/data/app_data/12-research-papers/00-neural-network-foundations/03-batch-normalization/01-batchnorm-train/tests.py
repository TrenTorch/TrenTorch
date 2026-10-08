"""
pytest data/app_data/12-research-papers/00-neural-network-foundations/03-batch-normalization/01-batchnorm-train/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-batchnorm-train")
batchnorm_train = _module.batchnorm_train


import numpy as np


def test_1_output_shape_matches_input():
    out, _, _ = batchnorm_train(np.ones((4, 3)), np.ones(3), np.zeros(3))
    assert out.shape == (4, 3)


def test_2_returns_batch_mean_and_variance():
    x = np.array([[1.0, 2.0], [3.0, 6.0]])
    _, mean, var = batchnorm_train(x, np.ones(2), np.zeros(2))
    np.testing.assert_allclose(mean, [2.0, 4.0])
    np.testing.assert_allclose(var, [1.0, 4.0])


def test_3_normalized_output_has_zero_mean_and_unit_variance():
    rng = np.random.default_rng(0)
    x = rng.normal(5.0, 3.0, size=(200, 4))
    out, _, _ = batchnorm_train(x, np.ones(4), np.zeros(4))
    np.testing.assert_allclose(out.mean(axis=0), 0.0, atol=1e-6)
    np.testing.assert_allclose(out.var(axis=0), 1.0, atol=1e-3)


def test_4_gamma_and_beta_scale_and_shift_the_output():
    x = np.array([[1.0], [3.0]])
    out, _, _ = batchnorm_train(x, np.array([2.0]), np.array([10.0]), eps=0.0)
    np.testing.assert_allclose(out, [[8.0], [12.0]])


def test_5_does_not_mutate_the_input():
    x = np.array([[1.0, 2.0], [3.0, 4.0]])
    batchnorm_train(x, np.ones(2), np.zeros(2))
    np.testing.assert_array_equal(x, [[1.0, 2.0], [3.0, 4.0]])


def test_6_matches_a_hand_computed_case():
    x = np.array([[1.0], [3.0]])
    out, _, _ = batchnorm_train(x, np.ones(1), np.zeros(1), eps=0.0)
    np.testing.assert_allclose(out, [[-1.0], [1.0]])

