"""
pytest tests.py
"""

import numpy as np

from _load import load_solution

_module = load_solution(__file__)
mixture_weights = _module.mixture_weights
epochs_per_source = _module.epochs_per_source
SIZES = np.array([900.0, 90.0, 10.0])


def test_1_temperature_one_is_proportional():
    assert np.allclose(mixture_weights(SIZES, 1.0), [0.9, 0.09, 0.01])


def test_2_hand_computed_temperature_two():
    s = np.sqrt(SIZES)
    assert np.allclose(mixture_weights(SIZES, 2.0), s / s.sum())


def test_3_high_temperature_approaches_uniform_and_low_sharpens():
    assert np.allclose(mixture_weights(SIZES, 1e6), 1 / 3, atol=1e-4)
    assert mixture_weights(SIZES, 0.2)[0] > 0.999


def test_4_weights_sum_to_one_and_keep_order():
    w = mixture_weights(SIZES, 3.0)
    assert np.isclose(w.sum(), 1.0) and w[0] > w[1] > w[2]


def test_5_epochs_hand_computed():
    e = epochs_per_source(SIZES, np.array([0.5, 0.25, 0.25]), 1000.0)
    assert np.allclose(e, [500 / 900, 250 / 90, 250 / 10])


def test_6_natural_mixture_gives_equal_epochs_everywhere():
    w = mixture_weights(SIZES, 1.0)
    e = epochs_per_source(SIZES, w, 5000.0)
    assert np.allclose(e, e[0])


def test_7_higher_temperature_repeats_small_sources_more_and_input_untouched():
    snap = SIZES.copy()
    low = epochs_per_source(SIZES, mixture_weights(SIZES, 1.0), 1e4)[2]
    high = epochs_per_source(SIZES, mixture_weights(SIZES, 3.0), 1e4)[2]
    assert high > low and np.array_equal(SIZES, snap)
