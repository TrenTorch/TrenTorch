"""
pytest data/app_data/99-potd/01-daily/31-engagement-slope-linreg/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"99-potd/01-daily/{Path(__file__).resolve().parent.name}")
fit_line = _module.fit_line

TOLERANCE = 1e-4


def test_example_matches_the_specs_worked_value():
    x = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
    y = np.array([50.0, 55.0, 65.0, 70.0, 80.0])
    w, b = fit_line(x, y)
    assert abs(w - 7.5) < TOLERANCE
    assert abs(b - 41.5) < TOLERANCE


def test_all_x_identical_gives_a_flat_line_at_mean_y():
    x = np.full(5, 3.0)
    y = np.array([10.0, 20.0, 30.0, 40.0, 50.0])
    w, b = fit_line(x, y)
    assert w == 0.0
    assert abs(b - 30.0) < TOLERANCE


def test_exact_linear_fit_recovers_the_true_line():
    x = np.arange(1, 20, dtype=float)
    true_w, true_b = 3.0, -7.0
    y = true_w * x + true_b
    w, b = fit_line(x, y)
    assert abs(w - true_w) < 1e-9
    assert abs(b - true_b) < 1e-9


def test_matches_a_reference_on_noisy_data():
    rng = np.random.default_rng(29)
    x = rng.uniform(0, 100, size=1000)
    y = 2.5 * x + 10 + rng.normal(0, 5, size=1000)
    w, b = fit_line(x, y)
    mean_x, mean_y = x.mean(), y.mean()
    expected_w = np.sum((x - mean_x) * (y - mean_y)) / np.sum((x - mean_x) ** 2)
    expected_b = mean_y - expected_w * mean_x
    assert abs(w - expected_w) < 1e-6
    assert abs(b - expected_b) < 1e-6
