"""
pytest tests.py
"""

import numpy as np

from _load import load_solution

_module = load_solution(__file__)
linear_betas = _module.linear_betas
alpha_bars = _module.alpha_bars
cosine_alpha_bars = _module.cosine_alpha_bars


def test_1_linear_betas_endpoints_and_spacing():
    b = linear_betas(5, 0.0, 0.4)
    assert np.allclose(b, [0.0, 0.1, 0.2, 0.3, 0.4])


def test_2_alpha_bars_hand_computed():
    assert np.allclose(alpha_bars(np.array([0.1, 0.2, 0.5])), [0.9, 0.72, 0.36])


def test_3_alpha_bars_decrease_monotonically_in_unit_interval():
    ab = alpha_bars(linear_betas(1000, 1e-4, 0.02))
    assert (np.diff(ab) < 0).all() and ab[0] > 0.999 and 0 < ab[-1] < 1e-3


def test_4_cosine_schedule_is_monotone_and_ends_near_zero():
    ab = cosine_alpha_bars(1000)
    assert (np.diff(ab) < 0).all() and ab[0] > 0.99 and ab[-1] < 1e-3 and len(ab) == 1000


def test_5_cosine_hand_computed_last_value():
    T, s = 10, 0.008
    f = lambda u: np.cos(((u / T) + s) / (1 + s) * np.pi / 2) ** 2
    assert np.isclose(cosine_alpha_bars(T, s)[-1], f(10) / f(0))


def test_6_cosine_keeps_more_signal_in_the_middle_than_linear_decays_fast_at_the_end():
    lin = alpha_bars(linear_betas(1000, 1e-4, 0.02))
    cos = cosine_alpha_bars(1000)
    # linear reaches near-zero signal much earlier than cosine
    assert np.argmax(lin < 1e-2) < np.argmax(cos < 1e-2)


def test_7_inputs_untouched():
    b = linear_betas(10, 0.01, 0.1)
    snap = b.copy()
    alpha_bars(b)
    assert np.array_equal(b, snap)
