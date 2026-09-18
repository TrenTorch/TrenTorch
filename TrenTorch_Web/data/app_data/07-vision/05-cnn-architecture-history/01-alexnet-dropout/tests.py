"""
pytest data/app_data/07-vision/05-cnn-architecture-history/01-alexnet-dropout/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

dropout_forward = load_solution(
    f"07-vision/05-cnn-architecture-history/{Path(__file__).resolve().parent.name}"
).dropout_forward


# --- Basic correctness (the two the "Run" button samples) -----------------


def test_01_output_shape_matches_input_shape():
    rng = np.random.default_rng(0)
    x = rng.normal(size=(4, 5))
    out = dropout_forward(x, p=0.5, rng=np.random.default_rng(1))
    assert out.shape == x.shape


def test_02_every_surviving_value_is_scaled_by_1_over_1_minus_p():
    x = np.ones((100,))
    out = dropout_forward(x, p=0.3, rng=np.random.default_rng(2))
    surviving = out[out != 0.0]
    assert np.allclose(surviving, 1.0 / (1.0 - 0.3))


# --- Shape / general-case coverage -----------------------------------


def test_03_dropped_values_are_exactly_zero():
    x = np.random.default_rng(3).normal(size=(500,))
    out = dropout_forward(x, p=0.4, rng=np.random.default_rng(4))
    dropped_mask = out == 0.0
    assert dropped_mask.sum() > 0  # at least some units were dropped
    assert np.all(out[~dropped_mask] != 0.0)


def test_04_roughly_p_fraction_of_units_are_dropped_over_many_units():
    x = np.ones((20000,))
    out = dropout_forward(x, p=0.5, rng=np.random.default_rng(5))
    fraction_dropped = (out == 0.0).mean()
    assert abs(fraction_dropped - 0.5) < 0.02  # law of large numbers, generous tolerance


# --- Parameter handling -------------------------------------------------


def test_05_p_zero_never_drops_anything_and_is_pure_identity():
    x = np.random.default_rng(6).normal(size=(50,))
    out = dropout_forward(x, p=0.0, rng=np.random.default_rng(7))
    assert np.allclose(out, x)


# --- Edge cases ---------------------------------------------------------


def test_06_reproducible_given_the_same_rng_state():
    x = np.random.default_rng(8).normal(size=(30,))
    out_a = dropout_forward(x, p=0.5, rng=np.random.default_rng(9))
    out_b = dropout_forward(x, p=0.5, rng=np.random.default_rng(9))
    assert np.array_equal(out_a, out_b)


# --- Array hygiene ------------------------------------------------------


def test_07_does_not_mutate_its_inputs():
    x = np.random.default_rng(10).normal(size=(20,))
    x_copy = x.copy()
    dropout_forward(x, p=0.5, rng=np.random.default_rng(11))
    assert np.array_equal(x, x_copy)


# --- Independent correctness oracle -----------------------------------


def test_08_expected_value_of_the_output_matches_the_input_by_law_of_large_numbers():
    # Dropout's randomness comes from an RNG stream, so its exact output
    # can't be cross-checked against a value baked from a *different*
    # RNG library (numpy vs. torch draw different bit streams even from
    # the "same" seed) -- that would be a false oracle claim. What CAN be
    # checked against real PyTorch (and against the mathematics of
    # inverted dropout itself, independent of any implementation) is the
    # defining property "inverted" dropout exists to guarantee: averaged
    # over many independent dropout masks, the expected output equals the
    # original input. This is exactly why `torch.nn.functional.dropout`
    # requires no rescaling at inference time -- training-time dropout is
    # already, in expectation, the identity function.
    x = np.full((10000,), 3.5)
    p = 0.25
    out = dropout_forward(x, p=p, rng=np.random.default_rng(12))
    assert abs(out.mean() - 3.5) < 0.05
