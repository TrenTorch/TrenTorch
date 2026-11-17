"""
pytest tests.py
"""

from _load import load_solution

_module = load_solution(__file__)
CircuitBreaker = _module.CircuitBreaker


def test_1_starts_closed_and_allows_calls():
    cb = CircuitBreaker(3, 10.0)
    assert cb.state == "closed" and cb.allow(0.0)


def test_2_opens_after_consecutive_failures():
    cb = CircuitBreaker(3, 10.0)
    for t in (1.0, 2.0, 3.0):
        cb.record_failure(t)
    assert cb.state == "open" and not cb.allow(4.0)


def test_3_success_resets_the_failure_count():
    cb = CircuitBreaker(3, 10.0)
    cb.record_failure(1.0)
    cb.record_failure(2.0)
    cb.record_success(3.0)
    cb.record_failure(4.0)
    cb.record_failure(5.0)
    assert cb.state == "closed"


def test_4_cooldown_moves_to_half_open_and_allows_one_trial():
    cb = CircuitBreaker(1, 10.0)
    cb.record_failure(0.0)
    assert not cb.allow(9.9) and cb.allow(10.0) and cb.state == "half_open"
    assert not cb.allow(10.1)


def test_5_trial_success_closes_the_circuit():
    cb = CircuitBreaker(1, 5.0)
    cb.record_failure(0.0)
    assert cb.allow(5.0)
    cb.record_success(5.5)
    assert cb.state == "closed" and cb.allow(6.0)


def test_6_trial_failure_reopens_with_a_fresh_cooldown():
    cb = CircuitBreaker(1, 5.0)
    cb.record_failure(0.0)
    assert cb.allow(5.0)
    cb.record_failure(5.5)
    assert cb.state == "open" and not cb.allow(10.0) and cb.allow(10.5)


def test_7_failures_while_closed_below_threshold_do_not_block():
    cb = CircuitBreaker(5, 1.0)
    for t in range(4):
        cb.record_failure(float(t))
        assert cb.allow(float(t) + 0.1)
