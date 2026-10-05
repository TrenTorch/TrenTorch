"""
pytest tests.py
"""

from _load import load_solution

_module = load_solution(__file__)
import math

success_rate = _module.success_rate
wilson_interval = _module.wilson_interval


def test_1_success_rate():
    assert success_rate(3, 4) == 0.75 and success_rate(0, 0) == 0.0


def test_2_hand_computed_interval():
    lo, hi = wilson_interval(50, 100)
    assert math.isclose(lo, 0.4038, abs_tol=5e-4) and math.isclose(hi, 0.5962, abs_tol=5e-4)


def test_3_interval_stays_inside_zero_one_at_the_extremes():
    lo0, hi0 = wilson_interval(0, 10)
    lo1, hi1 = wilson_interval(10, 10)
    assert lo0 >= 0 and hi0 > 0.1 and hi1 <= 1.0 and lo1 < 0.9


def test_4_no_data_is_the_whole_interval():
    assert wilson_interval(0, 0) == (0.0, 1.0)


def test_5_more_data_narrows_the_interval():
    w_small = wilson_interval(6, 10)
    w_big = wilson_interval(600, 1000)
    assert (w_big[1] - w_big[0]) < (w_small[1] - w_small[0]) / 5


def test_6_interval_contains_the_point_estimate_and_is_symmetric_at_half():
    lo, hi = wilson_interval(30, 60)
    assert lo < 0.5 < hi and math.isclose((lo + hi) / 2, 0.5)


def test_7_larger_z_widens_the_interval():
    a, b = wilson_interval(20, 50, 1.64), wilson_interval(20, 50, 2.58)
    assert (b[1] - b[0]) > (a[1] - a[0])
