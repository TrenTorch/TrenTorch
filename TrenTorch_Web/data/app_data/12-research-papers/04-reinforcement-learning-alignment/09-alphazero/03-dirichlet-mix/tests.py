"""
pytest data/app_data/12-research-papers/04-reinforcement-learning-and-alignment/09-alphazero/03-dirichlet-mix/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-alphazero-dirichlet-mix")
dirichlet_mix = _module.dirichlet_mix


import numpy as np


def test_1_eps_zero_keeps_the_prior():
    np.testing.assert_allclose(dirichlet_mix(np.array([0.3, 0.7]), np.array([1.0, 0.0]), 0.0), [0.3, 0.7])


def test_2_eps_one_uses_only_the_noise():
    np.testing.assert_allclose(dirichlet_mix(np.array([0.3, 0.7]), np.array([1.0, 0.0]), 1.0), [1.0, 0.0])


def test_3_matches_a_hand_value():
    np.testing.assert_allclose(dirichlet_mix(np.array([1.0, 0.0]), np.array([0.0, 1.0]), 0.25), [0.75, 0.25])


def test_4_sums_to_one_when_inputs_do():
    out = dirichlet_mix(np.array([0.2, 0.8]), np.array([0.5, 0.5]), 0.3)
    assert abs(out.sum() - 1.0) < 1e-12


def test_5_keeps_the_shape():
    assert dirichlet_mix(np.ones(4) / 4, np.ones(4) / 4, 0.1).shape == (4,)


def test_6_does_not_mutate_inputs():
    P = np.array([0.5, 0.5])
    dirichlet_mix(P, np.array([1.0, 0.0]), 0.5)
    np.testing.assert_array_equal(P, [0.5, 0.5])

