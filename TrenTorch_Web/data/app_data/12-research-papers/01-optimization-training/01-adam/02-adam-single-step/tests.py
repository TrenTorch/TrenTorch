"""
pytest data/app_data/12-research-papers/01-optimization-and-training/01-adam/02-adam-single-step/tests.py
"""

import math
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-adam-single-step")
adam_step = _module.adam_step


# ---- 1-2: basic correctness ----


def test_1_first_step_moves_by_about_the_learning_rate():
    theta, _, _ = adam_step(1.0, 2.0, 0.0, 0.0, t=1, lr=0.1)
    assert math.isclose(theta, 0.9, rel_tol=1e-6)


def test_2_returns_updated_moments_too():
    _, m, v = adam_step(1.0, 2.0, 0.0, 0.0, t=1, lr=0.1)
    assert math.isclose(m, 0.2)
    assert math.isclose(v, 0.004)


# ---- shape / general-case coverage ----


def test_3_works_on_numpy_arrays():
    theta, m, v = adam_step(
        np.array([1.0, -1.0]), np.array([2.0, -2.0]), np.zeros(2), np.zeros(2), t=1, lr=0.1
    )
    np.testing.assert_allclose(theta, [0.9, -0.9], rtol=1e-6)
    assert m.shape == (2,) and v.shape == (2,)


# ---- edge cases ----


def test_4_zero_gradient_leaves_theta_unchanged_on_first_step():
    theta, _, _ = adam_step(3.0, 0.0, 0.0, 0.0, t=1, lr=0.1)
    assert theta == 3.0


def test_5_first_step_size_is_independent_of_gradient_magnitude():
    small, _, _ = adam_step(0.0, 0.01, 0.0, 0.0, t=1, lr=0.1)
    large, _, _ = adam_step(0.0, 1000.0, 0.0, 0.0, t=1, lr=0.1)
    assert math.isclose(abs(small), 0.1, rel_tol=1e-6)
    assert math.isclose(abs(large), 0.1, rel_tol=1e-6)


# ---- mutation-catching ----


def test_6_bias_correction_is_applied():
    # Without bias correction the step would be lr * 0.2 / 2 = 0.01, not 0.1.
    theta, _, _ = adam_step(0.0, 2.0, 0.0, 0.0, t=1, lr=0.1)
    assert not math.isclose(theta, -0.01, rel_tol=1e-3)
    assert math.isclose(theta, -0.1, rel_tol=1e-6)


def test_7_step_direction_opposes_the_gradient():
    theta, _, _ = adam_step(0.0, 5.0, 0.0, 0.0, t=1, lr=0.1)
    assert theta < 0


# ---- independent oracle ----


def test_8_matches_a_hand_computed_second_step():
    # Step 1 from theta=1, g=2 gives m=0.2, v=0.004 and theta=0.9.
    theta1, m1, v1 = adam_step(1.0, 2.0, 0.0, 0.0, t=1, lr=0.1)
    # Step 2 with g=1.8: m=0.36, v=0.007236, m_hat=1.8947, v_hat=3.6197
    theta2, _, _ = adam_step(theta1, 1.8, m1, v1, t=2, lr=0.1)
    assert abs(theta2 - 0.8004) < 1e-3
