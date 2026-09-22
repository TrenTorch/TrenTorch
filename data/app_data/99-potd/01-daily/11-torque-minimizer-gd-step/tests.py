"""
pytest data/app_data/99-potd/01-daily/11-torque-minimizer-gd-step/tests.py
"""

import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"99-potd/01-daily/{Path(__file__).resolve().parent.name}")
gd_step = _module.gd_step

TOLERANCE = 1e-6


def _reference(a, b, c, theta_0, eta):
    grad = 2 * a * theta_0 + b
    theta_1 = theta_0 - eta * grad
    return theta_1, a * theta_1**2 + b * theta_1 + c


def test_example_matches_the_specs_worked_values():
    theta_1, cost = gd_step(1.0, -4.0, 5.0, 0.0, 0.1)
    assert abs(theta_1 - 0.4) < TOLERANCE
    assert abs(cost - 3.56) < TOLERANCE


def test_negative_a_still_reports_one_mechanical_step():
    theta_1, cost = gd_step(-1.0, 0.0, 0.0, 1.0, 0.1)
    expected = _reference(-1.0, 0.0, 0.0, 1.0, 0.1)
    assert abs(theta_1 - expected[0]) < TOLERANCE
    assert abs(cost - expected[1]) < TOLERANCE


def test_theta_already_at_the_vertex_does_not_move():
    a, b = 2.0, -8.0
    vertex = -b / (2 * a)
    theta_1, cost = gd_step(a, b, 0.0, vertex, 0.5)
    assert abs(theta_1 - vertex) < TOLERANCE


def test_very_small_eta_takes_a_tiny_step():
    theta_1, _ = gd_step(1.0, 0.0, 0.0, 10.0, 1e-6)
    # grad = 20.0, step = 1e-6 * 20.0 = 2e-5
    assert abs(theta_1 - (10.0 - 2e-5)) < 1e-9


def test_matches_a_reference_on_random_parameters():
    rng = random.Random(20260923)
    for _ in range(50):
        a = rng.uniform(-100, 100)
        if abs(a) < 1e-3:
            a = 1.0
        b = rng.uniform(-100, 100)
        c = rng.uniform(-100, 100)
        theta_0 = rng.uniform(-100, 100)
        eta = rng.uniform(1e-3, 1.0)
        got = gd_step(a, b, c, theta_0, eta)
        expected = _reference(a, b, c, theta_0, eta)
        assert abs(got[0] - expected[0]) < TOLERANCE
        assert abs(got[1] - expected[1]) < TOLERANCE
