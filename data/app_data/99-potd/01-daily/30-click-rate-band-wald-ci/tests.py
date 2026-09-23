"""
pytest data/app_data/99-potd/01-daily/30-click-rate-band-wald-ci/tests.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"99-potd/01-daily/{Path(__file__).resolve().parent.name}")
click_rate_band = _module.click_rate_band

TOLERANCE = 1e-4


def test_example_matches_the_specs_worked_value():
    p_hat, lower, upper = click_rate_band(1000, 45)
    assert abs(p_hat - 0.045) < TOLERANCE
    assert abs(lower - 0.032151) < TOLERANCE
    assert abs(upper - 0.057849) < TOLERANCE


def test_zero_clicks_collapses_the_interval_to_the_origin():
    p_hat, lower, upper = click_rate_band(1000, 0)
    assert p_hat == 0.0
    assert lower == 0.0
    assert upper == 0.0


def test_all_clicks_collapses_the_interval_to_one():
    p_hat, lower, upper = click_rate_band(1000, 1000)
    assert p_hat == 1.0
    assert lower == 1.0
    assert upper == 1.0


def test_interval_is_symmetric_around_p_hat():
    p_hat, lower, upper = click_rate_band(500, 100)
    assert abs((p_hat - lower) - (upper - p_hat)) < 1e-9


def test_large_n_stays_precise():
    p_hat, lower, upper = click_rate_band(10**9, 5 * 10**8)
    assert abs(p_hat - 0.5) < 1e-9
    assert lower < 0.5 < upper
