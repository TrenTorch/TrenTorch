"""
pytest data/app_data/01-classical-ml/07-evaluation/06-bayesian-optimization/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"01-classical-ml/07-evaluation/{Path(__file__).resolve().parent.name}")
expected_improvement = _module.expected_improvement
propose_next_point = _module.propose_next_point


def test_ei_is_zero_when_std_is_zero():
    mean = np.array([10.0, 0.0, -5.0])
    std = np.array([0.0, 0.0, 0.0])
    result = expected_improvement(mean, std, best_so_far=0.0)
    assert np.allclose(result, 0.0)


def test_ei_at_z_equals_zero_matches_hand_computation():
    # mean - best_so_far - xi = 0 exactly -> z=0, EI = std * phi(0)
    mean = np.array([1.01])
    std = np.array([2.0])
    result = expected_improvement(mean, std, best_so_far=1.0, xi=0.01)
    expected = 2.0 * (1.0 / np.sqrt(2 * np.pi))
    assert np.isclose(result[0], expected)


def test_ei_increases_with_larger_mean_above_best_so_far():
    std = np.array([1.0, 1.0])
    low_mean = expected_improvement(np.array([0.0]), std[:1], best_so_far=0.0)
    high_mean = expected_improvement(np.array([5.0]), std[:1], best_so_far=0.0)
    assert high_mean[0] > low_mean[0]


def test_ei_increases_with_larger_std_at_the_same_mean():
    # Exploration value: at a fixed (unimpressive) mean, more
    # uncertainty should mean more potential upside.
    mean = np.array([0.0])
    small_std = expected_improvement(mean, np.array([0.1]), best_so_far=0.0)
    large_std = expected_improvement(mean, np.array([5.0]), best_so_far=0.0)
    assert large_std[0] > small_std[0]


def test_ei_never_negative():
    rng = np.random.default_rng(0)
    mean = rng.normal(size=20)
    std = np.abs(rng.normal(size=20)) + 0.01
    result = expected_improvement(mean, std, best_so_far=0.3)
    assert np.all(result >= -1e-10)


def test_propose_next_point_explores_the_gap_between_two_seed_points():
    # Two seed points far from the true peak of a simple downward
    # parabola (-(x-0.5)^2) -- Bayesian optimization should propose
    # something in the unexplored middle, near the actual optimum,
    # not right next to either seed point.
    input_train = np.array([[0.1], [0.9]])
    targets_train = np.array([-((0.1 - 0.5) ** 2), -((0.9 - 0.5) ** 2)])
    candidates = np.linspace(0.0, 1.0, 50).reshape(-1, 1)

    idx = propose_next_point(
        input_train, targets_train, candidates, length_scale=0.3, variance=1.0, noise=1e-6
    )
    proposed_x = candidates[idx, 0]
    assert 0.3 < proposed_x < 0.7


def test_zero_std_guard_is_not_dropped():
    # Directly targets a mutant that removes the std>0 guard: dividing
    # by std=0 produces NaN or +/-inf, which would corrupt the
    # candidate-selection argmax entirely.
    mean = np.array([5.0, 0.0, -5.0])
    std = np.array([0.0, 1.0, 0.0])
    result = expected_improvement(mean, std, best_so_far=0.0)
    assert np.all(np.isfinite(result))
    assert result[0] == 0.0 and result[2] == 0.0
