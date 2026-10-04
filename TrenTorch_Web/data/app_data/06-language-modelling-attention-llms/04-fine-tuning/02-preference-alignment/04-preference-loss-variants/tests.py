"""
pytest tests.py
"""

import numpy as np

from _load import load_solution

_module = load_solution(__file__)
ipo_loss = _module.ipo_loss
simpo_loss = _module.simpo_loss


def test_1_ipo_is_zero_at_the_target_margin():
    tau = 0.5  # target margin 1.0
    assert np.isclose(ipo_loss(np.array([1.0]), np.array([0.0]), np.array([0.0]), np.array([0.0]), tau), 0.0)


def test_2_ipo_hand_computed_and_penalizes_overshoot():
    args = (np.array([0.0]), np.array([0.0]))
    small = ipo_loss(np.array([0.2]), np.array([0.0]), *args, tau=0.5)
    huge = ipo_loss(np.array([3.0]), np.array([0.0]), *args, tau=0.5)
    assert np.isclose(small, (0.2 - 1.0) ** 2) and np.isclose(huge, (3.0 - 1.0) ** 2)


def test_3_ipo_uses_the_reference_log_ratio():
    a = ipo_loss(np.array([-9.0]), np.array([-11.0]), np.array([-10.0]), np.array([-10.0]), 1.0)
    b = ipo_loss(np.array([-9.0]), np.array([-11.0]), np.array([-9.0]), np.array([-11.0]), 1.0)
    assert np.isclose(a, (2.0 - 0.5) ** 2) and np.isclose(b, (0.0 - 0.5) ** 2)


def test_4_simpo_hand_computed():
    # per-token: chosen -1, rejected -2 ; z = 2 * 1 - 0.5 = 1.5
    loss = simpo_loss(np.array([-4.0]), np.array([-8.0]), np.array([4]), np.array([4]), beta=2.0, gamma=0.5)
    assert np.isclose(loss, np.log(1 + np.exp(-1.5)))


def test_5_simpo_normalizes_by_length():
    # same per-token quality, different lengths => same loss
    a = simpo_loss(np.array([-5.0]), np.array([-10.0]), np.array([5]), np.array([5]), 1.0, 0.0)
    b = simpo_loss(np.array([-50.0]), np.array([-100.0]), np.array([50]), np.array([50]), 1.0, 0.0)
    assert np.isclose(a, b)


def test_6_simpo_margin_raises_the_loss_and_is_reference_free():
    base = simpo_loss(np.array([-3.0]), np.array([-6.0]), np.array([3]), np.array([3]), 1.0, 0.0)
    with_margin = simpo_loss(np.array([-3.0]), np.array([-6.0]), np.array([3]), np.array([3]), 1.0, 1.0)
    assert with_margin > base


def test_7_vectorised_means_and_no_mutation():
    rng = np.random.RandomState(0)
    pc, pr, rc, rr = (rng.randn(8) for _ in range(4))
    lc, lr = rng.randint(2, 9, 8), rng.randint(2, 9, 8)
    snap = pc.copy()
    h = (pc - rc) - (pr - rr)
    assert np.isclose(ipo_loss(pc, pr, rc, rr, 0.25), np.mean((h - 2.0) ** 2))
    z = 1.5 * (pc / lc - pr / lr) - 0.3
    assert np.isclose(simpo_loss(pc, pr, lc, lr, 1.5, 0.3), np.mean(np.log1p(np.exp(-z))))
    assert np.array_equal(pc, snap)
