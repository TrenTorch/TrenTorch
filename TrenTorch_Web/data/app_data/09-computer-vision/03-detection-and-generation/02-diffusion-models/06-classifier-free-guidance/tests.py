"""
pytest tests.py
"""

import numpy as np

from _load import load_solution

_module = load_solution(__file__)
cfg_combine = _module.cfg_combine
drop_condition = _module.drop_condition
U, C = np.array([1.0, 2.0]), np.array([3.0, 0.0])


def test_1_w_zero_is_unconditional_and_w_one_is_conditional():
    assert np.allclose(cfg_combine(U, C, 0.0), U) and np.allclose(cfg_combine(U, C, 1.0), C)


def test_2_hand_computed_extrapolation():
    assert np.allclose(cfg_combine(U, C, 3.0), [1 + 3 * 2, 2 + 3 * -2])


def test_3_identical_predictions_ignore_the_scale():
    assert np.allclose(cfg_combine(U, U, 7.5), U)


def test_4_linear_in_w():
    a, b = cfg_combine(U, C, 2.0), cfg_combine(U, C, 4.0)
    assert np.allclose(cfg_combine(U, C, 3.0), (a + b) / 2)


def test_5_drop_condition_matches_the_seeded_draw():
    ids = np.arange(10)
    out = drop_condition(ids, 0.3, -1, np.random.RandomState(0))
    u = np.random.RandomState(0).random_sample(10)
    assert np.array_equal(out, np.where(u < 0.3, -1, ids))


def test_6_empirical_drop_rate_and_extremes():
    ids = np.arange(20000)
    out = drop_condition(ids, 0.1, -1, np.random.RandomState(1))
    assert abs((out == -1).mean() - 0.1) < 0.01
    assert (drop_condition(ids, 0.0, -1, np.random.RandomState(2)) == ids).all()
    assert (drop_condition(ids, 1.0, -1, np.random.RandomState(3)) == -1).all()


def test_7_inputs_untouched():
    ids = np.arange(8)
    snap = ids.copy()
    drop_condition(ids, 0.5, -1, np.random.RandomState(4))
    u, c = U.copy(), C.copy()
    cfg_combine(U, C, 2.0)
    assert np.array_equal(ids, snap) and np.array_equal(U, u) and np.array_equal(C, c)
