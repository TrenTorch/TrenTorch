"""
pytest data/app_data/12-research-papers/01-optimization-and-training/01-adam/03-adam-minimize/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-adam-minimize")
adam_minimize = _module.adam_minimize


def quadratic_grad(x):
    return 2 * x


# ---- 1-2: basic correctness ----


def test_1_trajectory_length_is_steps_plus_one():
    trajectory = adam_minimize(quadratic_grad, 1.0, steps=5)
    assert len(trajectory) == 6


def test_2_converges_toward_the_minimum_of_x_squared():
    trajectory = adam_minimize(quadratic_grad, 3.0, steps=500, lr=0.05)
    assert abs(float(trajectory[-1])) < 0.05


# ---- shape / general-case coverage ----


def test_3_first_element_is_the_starting_point():
    trajectory = adam_minimize(quadratic_grad, 2.5, steps=3)
    assert float(trajectory[0]) == 2.5


def test_4_works_on_a_vector_parameter():
    trajectory = adam_minimize(lambda x: 2 * x, np.array([1.0, -2.0]), steps=400, lr=0.05)
    np.testing.assert_allclose(trajectory[-1], [0.0, 0.0], atol=0.05)


# ---- edge cases ----


def test_5_zero_steps_returns_only_the_start():
    trajectory = adam_minimize(quadratic_grad, 4.0, steps=0)
    assert len(trajectory) == 1
    assert float(trajectory[0]) == 4.0


def test_6_already_at_minimum_stays_put():
    trajectory = adam_minimize(quadratic_grad, 0.0, steps=10)
    assert all(abs(float(x)) < 1e-12 for x in trajectory)


# ---- mutation-catching ----


def test_7_moves_against_the_gradient():
    trajectory = adam_minimize(quadratic_grad, 1.0, steps=1, lr=0.1)
    assert float(trajectory[1]) < float(trajectory[0])


def test_8_each_step_uses_the_updated_position():
    # A wrong implementation recomputing from theta0 each step would stop moving after step 1.
    trajectory = adam_minimize(quadratic_grad, 1.0, steps=3, lr=0.1)
    assert float(trajectory[2]) < float(trajectory[1])


# ---- independent oracle ----


def test_9_matches_a_hand_computed_first_step():
    # From theta=1, g=2, lr=0.1: first Adam step moves to 0.9.
    trajectory = adam_minimize(quadratic_grad, 1.0, steps=1, lr=0.1)
    assert abs(float(trajectory[1]) - 0.9) < 1e-6
