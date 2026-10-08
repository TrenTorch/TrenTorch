"""
pytest data/app_data/12-research-papers/00-neural-network-foundations/04-layer-normalization/02-layernorm-affine/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-layernorm-affine")
layernorm = _module.layernorm


import numpy as np


def test_1_identity_affine_matches_plain_normalization():
    x = np.array([[1.0, 2.0, 3.0]])
    out = layernorm(x, np.ones(3), np.zeros(3))
    np.testing.assert_allclose(out.mean(axis=-1), 0.0, atol=1e-9)


def test_2_gamma_scales_each_feature():
    x = np.array([[5.0, 7.0]])
    out = layernorm(x, np.array([2.0, 3.0]), np.zeros(2), eps=0.0)
    np.testing.assert_allclose(out, [[-2.0, 3.0]])


def test_3_beta_shifts_each_feature():
    x = np.array([[5.0, 7.0]])
    out = layernorm(x, np.ones(2), np.array([10.0, 20.0]), eps=0.0)
    np.testing.assert_allclose(out, [[9.0, 21.0]])


def test_4_each_example_is_independent_of_the_batch():
    x = np.array([[1.0, 2.0], [100.0, 200.0]])
    together = layernorm(x, np.ones(2), np.zeros(2))
    alone = layernorm(x[:1], np.ones(2), np.zeros(2))
    np.testing.assert_allclose(together[0], alone[0])


def test_5_works_on_three_dimensional_input():
    out = layernorm(np.ones((2, 5, 4)), np.ones(4), np.zeros(4))
    assert out.shape == (2, 5, 4)


def test_6_does_not_mutate_the_input():
    x = np.array([[1.0, 2.0]])
    layernorm(x, np.ones(2), np.zeros(2))
    np.testing.assert_array_equal(x, [[1.0, 2.0]])

