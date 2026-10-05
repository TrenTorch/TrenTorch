"""
pytest tests.py
"""

from _load import load_solution

_module = load_solution(__file__)
TokenBucket = _module.TokenBucket


def test_1_burst_up_to_capacity_then_blocked():
    b = TokenBucket(3, 1.0)
    assert [b.try_acquire(0.0) for _ in range(4)] == [True, True, True, False]


def test_2_refill_over_time():
    b = TokenBucket(2, 1.0)
    b.try_acquire(0.0, 2)
    assert not b.try_acquire(0.5) and b.try_acquire(1.0)


def test_3_tokens_never_exceed_capacity():
    b = TokenBucket(2, 10.0)
    b.try_acquire(100.0, 0)
    assert b.tokens == 2.0


def test_4_failed_acquire_does_not_consume_tokens():
    b = TokenBucket(2, 0.0)
    assert not b.try_acquire(0.0, 3) and b.tokens == 2.0


def test_5_steady_state_rate():
    b = TokenBucket(1, 2.0)
    granted = sum(b.try_acquire(t * 0.5) for t in range(1, 21))
    assert granted == 20


def test_6_fractional_tokens_accumulate():
    b = TokenBucket(1, 0.5)
    b.try_acquire(0.0)
    assert not b.try_acquire(1.0) and b.try_acquire(2.0)


def test_7_expensive_actions_cost_more():
    b = TokenBucket(5, 1.0)
    assert b.try_acquire(0.0, 4) and not b.try_acquire(0.0, 2) and b.try_acquire(1.0, 2)
