"""
pytest data/app_data/12-research-papers/00-neural-network-foundations/03-batch-normalization/03-running-stats-update/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-batchnorm-running-stats")
update_running_stats = _module.update_running_stats


import numpy as np


def test_1_moves_running_mean_toward_batch_mean():
    m, _ = update_running_stats(np.array([0.0]), np.array([1.0]), np.array([10.0]), np.array([1.0]), momentum=0.1)
    np.testing.assert_allclose(m, [1.0])


def test_2_moves_running_var_toward_batch_var():
    _, v = update_running_stats(np.array([0.0]), np.array([1.0]), np.array([0.0]), np.array([11.0]), momentum=0.1)
    np.testing.assert_allclose(v, [2.0])


def test_3_momentum_one_replaces_the_running_stats():
    m, v = update_running_stats(np.array([5.0]), np.array([5.0]), np.array([1.0]), np.array([2.0]), momentum=1.0)
    np.testing.assert_allclose(m, [1.0])
    np.testing.assert_allclose(v, [2.0])


def test_4_momentum_zero_keeps_the_running_stats():
    m, v = update_running_stats(np.array([5.0]), np.array([5.0]), np.array([1.0]), np.array([2.0]), momentum=0.0)
    np.testing.assert_allclose(m, [5.0])
    np.testing.assert_allclose(v, [5.0])


def test_5_works_on_vectors():
    m, _ = update_running_stats(np.zeros(3), np.ones(3), np.array([1.0, 2.0, 3.0]), np.ones(3), momentum=0.5)
    np.testing.assert_allclose(m, [0.5, 1.0, 1.5])


def test_6_does_not_mutate_the_inputs():
    rm = np.array([0.0])
    update_running_stats(rm, np.array([1.0]), np.array([4.0]), np.array([1.0]))
    np.testing.assert_array_equal(rm, [0.0])

