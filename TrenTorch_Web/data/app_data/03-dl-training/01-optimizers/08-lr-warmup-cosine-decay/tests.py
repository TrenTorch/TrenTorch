"""
pytest data/app_data/03-dl-training/01-optimizers/08-lr-warmup-cosine-decay/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"03-dl-training/01-optimizers/{Path(__file__).resolve().parent.name}")
linear_warmup_lr = _module.linear_warmup_lr
cosine_decay_lr = _module.cosine_decay_lr
warmup_cosine_lr = _module.warmup_cosine_lr


def test_linear_warmup_starts_at_zero():
    assert linear_warmup_lr(0, warmup_steps=10, base_lr=0.001) == 0.0


def test_linear_warmup_reaches_base_lr_exactly_at_warmup_steps():
    assert np.isclose(linear_warmup_lr(10, warmup_steps=10, base_lr=0.001), 0.001)


def test_linear_warmup_is_halfway_at_half_of_warmup_steps():
    assert np.isclose(linear_warmup_lr(5, warmup_steps=10, base_lr=0.001), 0.0005)


def test_linear_warmup_holds_at_base_lr_past_warmup_steps():
    assert np.isclose(linear_warmup_lr(50, warmup_steps=10, base_lr=0.001), 0.001)


def test_cosine_decay_starts_at_base_lr():
    assert np.isclose(cosine_decay_lr(0, total_steps=100, base_lr=0.001, min_lr=0.0), 0.001)


def test_cosine_decay_reaches_min_lr_exactly_at_total_steps():
    assert np.isclose(cosine_decay_lr(100, total_steps=100, base_lr=0.001, min_lr=0.0), 0.0, atol=1e-9)


def test_cosine_decay_holds_at_min_lr_past_total_steps():
    assert np.isclose(cosine_decay_lr(200, total_steps=100, base_lr=0.001, min_lr=0.0), 0.0, atol=1e-9)


def test_cosine_decay_is_symmetric_around_the_midpoint():
    # At progress = 0.5, cos(pi/2) = 0, so lr should be exactly the midpoint
    # between base_lr and min_lr.
    mid = cosine_decay_lr(50, total_steps=100, base_lr=0.001, min_lr=0.0002)
    assert np.isclose(mid, (0.001 + 0.0002) / 2.0)


def test_cosine_decay_respects_nonzero_min_lr():
    result = cosine_decay_lr(100, total_steps=100, base_lr=0.001, min_lr=0.0001)
    assert np.isclose(result, 0.0001)


def test_warmup_cosine_matches_pure_warmup_during_warmup_phase():
    for step in [0, 3, 7, 10]:
        expected = linear_warmup_lr(step, warmup_steps=10, base_lr=0.001)
        actual = warmup_cosine_lr(step, warmup_steps=10, total_steps=100, base_lr=0.001)
        assert np.isclose(actual, expected)


def test_warmup_cosine_is_continuous_at_the_warmup_boundary():
    just_before = warmup_cosine_lr(9, warmup_steps=10, total_steps=100, base_lr=0.001)
    at_boundary = warmup_cosine_lr(10, warmup_steps=10, total_steps=100, base_lr=0.001)
    assert at_boundary > just_before
    assert np.isclose(at_boundary, 0.001)


def test_warmup_cosine_reaches_min_lr_exactly_at_total_steps():
    result = warmup_cosine_lr(100, warmup_steps=10, total_steps=100, base_lr=0.001, min_lr=0.0)
    assert np.isclose(result, 0.0, atol=1e-9)


def test_warmup_cosine_matches_hand_computed_values_from_the_readme():
    # From the README's worked example: warmup_steps=10, total_steps=100, base_lr=0.001
    expected = {
        0: 0.0,
        5: 0.0005,
        10: 0.001,
        15: 0.000992403876506104,
        30: 0.000883022221559489,
        55: 0.0005,
        100: 0.0,
    }
    for step, exp_lr in expected.items():
        actual = warmup_cosine_lr(step, warmup_steps=10, total_steps=100, base_lr=0.001)
        assert np.isclose(actual, exp_lr, atol=1e-9), f"step={step}"


def test_warmup_cosine_is_monotonically_increasing_during_warmup():
    lrs = [warmup_cosine_lr(s, warmup_steps=10, total_steps=100, base_lr=0.001) for s in range(11)]
    assert all(lrs[i] <= lrs[i + 1] for i in range(len(lrs) - 1))


def test_warmup_cosine_is_monotonically_decreasing_during_decay():
    lrs = [warmup_cosine_lr(s, warmup_steps=10, total_steps=100, base_lr=0.001) for s in range(10, 101)]
    assert all(lrs[i] >= lrs[i + 1] for i in range(len(lrs) - 1))


def test_warmup_cosine_uses_rebased_step_for_decay_phase_not_global_step():
    # Directly targets a mutant that forgets to subtract warmup_steps before
    # calling cosine_decay_lr, i.e. passes the raw global step and total_steps
    # unchanged. That mutant would decay far too slowly right after warmup
    # ends, since it thinks only `step` (not `step - warmup_steps`) has
    # elapsed out of `total_steps` (not `total_steps - warmup_steps`).
    warmup_steps, total_steps, base_lr = 10, 20, 0.001
    # One step into decay (global step 11) with a short decay window (10 steps)
    # should already show noticeable decay, not be nearly flat at base_lr.
    result = warmup_cosine_lr(11, warmup_steps, total_steps, base_lr)
    correct_expected = cosine_decay_lr(1, total_steps - warmup_steps, base_lr)
    assert np.isclose(result, correct_expected)
    buggy_unrebased = cosine_decay_lr(11, total_steps, base_lr)
    assert not np.isclose(result, buggy_unrebased)
