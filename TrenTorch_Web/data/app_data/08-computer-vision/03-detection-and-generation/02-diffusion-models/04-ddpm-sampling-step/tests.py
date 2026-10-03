"""
pytest tests.py
"""

import numpy as np

from _load import load_solution

_module = load_solution(__file__)
ddpm_step = _module.ddpm_step
BETAS = np.array([0.1, 0.2, 0.3])
AB = np.cumprod(1 - BETAS)


def test_1_hand_computed_mean_without_noise_at_t0():
    out = ddpm_step(np.array([2.0]), np.array([1.0]), 0, BETAS, AB, np.array([99.0]))
    # beta=0.1 ; ab0=0.9 ; mean=(2 - 0.1/sqrt(0.1)) / sqrt(0.9)
    assert np.allclose(out, [(2.0 - 0.1 / np.sqrt(0.1)) / np.sqrt(0.9)])


def test_2_noise_is_added_for_t_above_zero():
    base = ddpm_step(np.array([1.0]), np.array([0.0]), 2, BETAS, AB, np.array([0.0]))
    noisy = ddpm_step(np.array([1.0]), np.array([0.0]), 2, BETAS, AB, np.array([1.0]))
    assert np.isclose(noisy[0] - base[0], np.sqrt(0.3))


def test_3_no_noise_at_the_last_step_even_if_z_is_given():
    a = ddpm_step(np.array([1.0]), np.array([0.2]), 0, BETAS, AB, np.array([5.0]))
    b = ddpm_step(np.array([1.0]), np.array([0.2]), 0, BETAS, AB, np.array([-5.0]))
    assert np.array_equal(a, b)


def test_4_mean_with_true_noise_equals_the_posterior_mean_of_the_forward_process():
    rng = np.random.RandomState(0)
    x0, eps = rng.randn(5), rng.randn(5)
    t = 2
    xt = np.sqrt(AB[t]) * x0 + np.sqrt(1 - AB[t]) * eps
    out = ddpm_step(xt, eps, t, BETAS, AB, np.zeros(5))
    alpha, ab_prev = 1 - BETAS[t], AB[t - 1]
    posterior_mean = (np.sqrt(ab_prev) * BETAS[t] / (1 - AB[t])) * x0 + (np.sqrt(alpha) * (1 - ab_prev) / (1 - AB[t])) * xt
    assert np.allclose(out, posterior_mean)


def test_5_zero_noise_prediction_just_rescales():
    out = ddpm_step(np.array([2.0]), np.array([0.0]), 1, BETAS, AB, np.zeros(1))
    assert np.allclose(out, [2.0 / np.sqrt(0.8)])


def test_6_shape_is_preserved():
    x = np.zeros((2, 3, 3))
    assert ddpm_step(x, x, 1, BETAS, AB, x).shape == (2, 3, 3)


def test_7_inputs_untouched():
    x, e, z = (np.random.RandomState(i).randn(4) for i in range(3))
    snaps = [x.copy(), e.copy(), z.copy()]
    ddpm_step(x, e, 1, BETAS, AB, z)
    assert all(np.array_equal(a, b) for a, b in zip((x, e, z), snaps))
