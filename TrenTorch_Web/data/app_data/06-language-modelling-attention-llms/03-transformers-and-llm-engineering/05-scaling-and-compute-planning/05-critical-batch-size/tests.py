"""
pytest tests.py
"""

import numpy as np

from _load import load_solution

_module = load_solution(__file__)
gradient_noise_scale = _module.gradient_noise_scale
steps_to_target = _module.steps_to_target


def test_1_hand_computed():
    g = np.array([[1.0, 0.0], [3.0, 0.0]])
    # mean [2, 0]; sum sq dev = 1 + 1 = 2 ; /(n-1)=2 ; ||mean||^2 = 4
    assert np.isclose(gradient_noise_scale(g), 0.5)


def test_2_pure_signal_has_zero_noise():
    g = np.tile(np.array([1.0, 2.0, 3.0]), (5, 1))
    assert np.isclose(gradient_noise_scale(g), 0.0)


def test_3_more_noise_raises_the_scale():
    rng = np.random.RandomState(0)
    signal = np.array([1.0, 1.0, 1.0, 1.0])
    low = signal + rng.randn(500, 4) * 0.5
    high = signal + rng.randn(500, 4) * 5.0
    assert gradient_noise_scale(high) > 10 * gradient_noise_scale(low)


def test_4_scale_invariant_to_gradient_units():
    g = np.random.RandomState(1).randn(50, 6) + 2.0
    assert np.isclose(gradient_noise_scale(g), gradient_noise_scale(g * 1000.0))


def test_5_steps_at_critical_batch_is_twice_the_minimum():
    assert np.isclose(steps_to_target(512, 1000, 512), 2000)


def test_6_steps_shrink_with_batch_but_examples_grow():
    small, big = steps_to_target(64, 1000, 512), steps_to_target(4096, 1000, 512)
    assert big < small and big * 4096 > small * 64


def test_7_large_batch_approaches_the_minimum_steps_and_input_untouched():
    g = np.random.RandomState(2).randn(20, 3)
    snap = g.copy()
    gradient_noise_scale(g)
    assert np.isclose(steps_to_target(1e9, 1000, 512), 1000, rtol=1e-6)
    assert np.array_equal(g, snap)
