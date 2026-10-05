"""
pytest tests.py
"""

from _load import load_solution

_module = load_solution(__file__)
import random

backoff_delays = _module.backoff_delays
total_wait = _module.total_wait


def test_1_deterministic_schedule():
    assert backoff_delays(4, 1.0, 2.0, 100.0) == [1.0, 2.0, 4.0, 8.0]


def test_2_cap_limits_growth():
    assert backoff_delays(5, 1.0, 3.0, 10.0) == [1.0, 3.0, 9.0, 10.0, 10.0]


def test_3_zero_retries():
    assert backoff_delays(0, 1.0, 2.0, 5.0) == [] and total_wait([]) == 0.0


def test_4_jitter_uses_one_draw_per_retry_in_order():
    got = backoff_delays(3, 2.0, 2.0, 100.0, random.Random(5))
    r = random.Random(5)
    assert got == [2.0 * r.random(), 4.0 * r.random(), 8.0 * r.random()]


def test_5_jittered_delays_never_exceed_the_capped_delay():
    got = backoff_delays(8, 1.0, 2.0, 10.0, random.Random(0))
    assert all(0.0 <= d <= min(10.0, 2.0 ** k) for k, d in enumerate(got))


def test_6_total_wait_hand_computed():
    assert total_wait([1.0, 2.0, 4.0]) == 7.0


def test_7_jitter_lowers_the_expected_total_wait():
    plain = total_wait(backoff_delays(6, 1.0, 2.0, 100.0))
    avg = sum(total_wait(backoff_delays(6, 1.0, 2.0, 100.0, random.Random(s))) for s in range(300)) / 300
    assert 0.4 * plain < avg < 0.6 * plain
