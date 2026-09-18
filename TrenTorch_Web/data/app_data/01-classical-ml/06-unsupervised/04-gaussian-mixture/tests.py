"""
pytest data/app_data/01-classical-ml/06-unsupervised/04-gaussian-mixture/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"01-classical-ml/06-unsupervised/{Path(__file__).resolve().parent.name}")
gmm_e_step = _module.gmm_e_step
gmm_m_step = _module.gmm_m_step


def test_responsibilities_sum_to_one_per_sample():
    input = np.array([[0.0], [1.0], [10.0], [11.0]])
    weights = np.array([0.5, 0.5])
    means = np.array([[0.5], [10.5]])
    variances = np.ones((2, 1))
    responsibilities = gmm_e_step(input, weights, means, variances)
    assert np.allclose(responsibilities.sum(axis=1), 1.0)


def test_e_step_favors_the_closer_component():
    input = np.array([[0.0], [10.0]])
    weights = np.array([0.5, 0.5])
    means = np.array([[0.0], [10.0]])
    variances = np.ones((2, 1))
    responsibilities = gmm_e_step(input, weights, means, variances)
    assert responsibilities[0, 0] > responsibilities[0, 1]
    assert responsibilities[1, 1] > responsibilities[1, 0]


def test_e_step_matches_hand_computation_with_equal_variance_and_weight():
    # With equal weight and variance, the E-step reduces to a
    # normalized Gaussian-kernel similarity, hand-checkable exactly.
    input = np.array([[0.0]])
    weights = np.array([0.5, 0.5])
    means = np.array([[0.0], [2.0]])
    variances = np.ones((2, 1))
    responsibilities = gmm_e_step(input, weights, means, variances)
    unnorm_0 = np.exp(-0.5 * 0.0**2)
    unnorm_1 = np.exp(-0.5 * 2.0**2)
    expected_0 = unnorm_0 / (unnorm_0 + unnorm_1)
    assert np.isclose(responsibilities[0, 0], expected_0)


def test_m_step_with_hard_responsibilities_matches_plain_kmeans_average():
    # Responsibilities of exactly 0/1 (hard assignment) reduce the
    # weighted M-step average to a plain group mean -- the same answer
    # 02-kmeans-centroid-update would give.
    input = np.array([[0.0], [2.0], [10.0], [12.0]])
    responsibilities = np.array([[1.0, 0.0], [1.0, 0.0], [0.0, 1.0], [0.0, 1.0]])
    weights, means, variances = gmm_m_step(input, responsibilities)
    assert np.allclose(means, [[1.0], [11.0]])
    assert np.allclose(weights, [0.5, 0.5])


def test_m_step_weights_sum_to_one():
    rng = np.random.default_rng(0)
    input = rng.normal(size=(20, 2))
    raw = rng.random((20, 3))
    responsibilities = raw / raw.sum(axis=1, keepdims=True)
    weights, _, _ = gmm_m_step(input, responsibilities)
    assert np.isclose(weights.sum(), 1.0)


def test_m_step_uses_weighted_average_not_plain_average():
    # Directly targets a mutant that ignores responsibilities and just
    # averages every sample plainly: with heavily skewed (soft, non-0/1)
    # responsibilities, the weighted mean should sit close to the
    # heavily-weighted point, far from the plain unweighted average.
    input = np.array([[0.0], [100.0]])
    responsibilities = np.array([[0.99, 0.01], [0.01, 0.99]])
    _, means, _ = gmm_m_step(input, responsibilities)
    assert means[0, 0] < 5.0  # component 0 is 99% about the point at 0
    assert means[1, 0] > 95.0  # component 1 is 99% about the point at 100


def test_full_em_loop_recovers_two_well_separated_clusters():
    rng = np.random.default_rng(1)
    cluster0 = rng.normal(loc=-5.0, scale=0.5, size=(60, 2))
    cluster1 = rng.normal(loc=5.0, scale=0.5, size=(60, 2))
    input = np.vstack([cluster0, cluster1])

    weights = np.array([0.5, 0.5])
    means = np.array([[-4.0, -6.0], [6.0, 4.0]])  # deliberately imperfect start
    variances = np.ones((2, 2))

    for _ in range(15):
        responsibilities = gmm_e_step(input, weights, means, variances)
        weights, means, variances = gmm_m_step(input, responsibilities)

    sorted_means = means[np.argsort(means[:, 0])]
    assert np.allclose(sorted_means[0], [-5.0, -5.0], atol=0.3)
    assert np.allclose(sorted_means[1], [5.0, 5.0], atol=0.3)
