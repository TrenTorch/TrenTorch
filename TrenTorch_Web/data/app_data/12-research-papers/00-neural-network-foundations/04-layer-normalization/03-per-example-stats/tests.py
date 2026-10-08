"""
pytest data/app_data/12-research-papers/00-neural-network-foundations/04-layer-normalization/03-per-example-stats/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-layernorm-per-example-stats")
per_example_stats = _module.per_example_stats


import numpy as np


def test_1_output_shapes_are_one_per_example():
    means, variances = per_example_stats(np.ones((4, 3)))
    assert means.shape == (4,)
    assert variances.shape == (4,)


def test_2_means_are_row_means():
    means, _ = per_example_stats(np.array([[1.0, 3.0], [2.0, 6.0]]))
    np.testing.assert_allclose(means, [2.0, 4.0])


def test_3_variances_are_row_variances():
    _, variances = per_example_stats(np.array([[1.0, 3.0], [2.0, 6.0]]))
    np.testing.assert_allclose(variances, [1.0, 4.0])


def test_4_constant_rows_have_zero_variance():
    _, variances = per_example_stats(np.array([[5.0, 5.0, 5.0]]))
    np.testing.assert_allclose(variances, [0.0])


def test_5_statistics_are_not_shared_across_examples():
    means, _ = per_example_stats(np.array([[0.0, 0.0], [10.0, 10.0]]))
    assert means[0] != means[1]


def test_6_does_not_mutate_the_input():
    x = np.array([[1.0, 2.0]])
    per_example_stats(x)
    np.testing.assert_array_equal(x, [[1.0, 2.0]])

