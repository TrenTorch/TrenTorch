"""
pytest data/app_data/07-vision/06-vision-transformer/05-classification-head/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

classification_head = load_solution(
    f"07-vision/06-vision-transformer/{Path(__file__).resolve().parent.name}"
).classification_head


# --- Basic correctness (the two the "Run" button samples) -----------------


def test_01_output_shape_is_num_classes():
    rng = np.random.default_rng(0)
    sequence = rng.normal(size=(10, 8))
    weight = rng.normal(size=(3, 8))
    bias = rng.normal(size=3)
    out = classification_head(sequence, weight, bias)
    assert out.shape == (3,)


def test_02_output_is_a_valid_probability_distribution():
    rng = np.random.default_rng(1)
    sequence = rng.normal(size=(6, 4))
    weight = rng.normal(size=(5, 4))
    bias = rng.normal(size=5)
    out = classification_head(sequence, weight, bias)
    assert np.all(out >= 0.0)
    assert np.isclose(out.sum(), 1.0)


# --- Shape / general-case coverage -----------------------------------


def test_03_only_position_zero_the_cls_token_affects_the_output():
    rng = np.random.default_rng(2)
    sequence = rng.normal(size=(6, 4))
    weight = rng.normal(size=(3, 4))
    bias = rng.normal(size=3)
    out_a = classification_head(sequence, weight, bias)
    sequence_modified = sequence.copy()
    sequence_modified[1:] = rng.normal(size=(5, 4))  # change every non-CLS position
    out_b = classification_head(sequence_modified, weight, bias)
    assert np.allclose(out_a, out_b)


def test_04_changing_the_cls_token_changes_the_output():
    rng = np.random.default_rng(3)
    sequence = rng.normal(size=(6, 4))
    weight = rng.normal(size=(3, 4))
    bias = rng.normal(size=3)
    out_a = classification_head(sequence, weight, bias)
    sequence_modified = sequence.copy()
    sequence_modified[0] = rng.normal(size=4)
    out_b = classification_head(sequence_modified, weight, bias)
    assert not np.allclose(out_a, out_b)


# --- Parameter handling -------------------------------------------------


def test_05_single_class_gives_a_degenerate_all_one_distribution():
    rng = np.random.default_rng(4)
    sequence = rng.normal(size=(4, 5))
    weight = rng.normal(size=(1, 5))
    bias = rng.normal(size=1)
    out = classification_head(sequence, weight, bias)
    assert out.shape == (1,)
    assert np.isclose(out[0], 1.0)


# --- Edge cases ---------------------------------------------------------


def test_06_single_token_sequence_is_just_its_own_cls_token():
    sequence = np.array([[1.0, 0.0]])
    weight = np.array([[1.0, 0.0], [0.0, 1.0]])
    bias = np.zeros(2)
    out = classification_head(sequence, weight, bias)
    assert out.shape == (2,)
    assert out[0] > out[1]  # logits [1, 0] -> class 0 more probable


# --- Array hygiene ------------------------------------------------------


def test_07_does_not_mutate_its_inputs():
    rng = np.random.default_rng(5)
    sequence = rng.normal(size=(5, 4))
    weight = rng.normal(size=(3, 4))
    bias = rng.normal(size=3)
    seq_copy, w_copy, b_copy = sequence.copy(), weight.copy(), bias.copy()
    classification_head(sequence, weight, bias)
    assert np.array_equal(sequence, seq_copy)
    assert np.array_equal(weight, w_copy)
    assert np.array_equal(bias, b_copy)


# --- Independent correctness oracle -----------------------------------


def test_08_matches_real_pytorch_linear_plus_softmax_on_the_cls_token_on_a_baked_reference_case():
    # Ground truth from the actual library, not our own derivation.
    # Generated once, offline, with:
    #   cls_out = torch.randn(3)
    #   weight = torch.randn(2, 3)
    #   bias = torch.randn(2)
    #   logits = torch.nn.functional.linear(cls_out, weight, bias)
    #   probs = torch.softmax(logits, dim=0)
    #
    # This test needs no torch installed to run -- the reference values
    # are baked in below.
    cls_token_row = np.array([0.9674, 0.6711, 0.5169])
    sequence = np.vstack([cls_token_row, np.zeros((4, 3))])  # rest of the sequence is irrelevant
    weight = np.array([[0.3077, -0.0911, -0.2627], [1.8645, -0.6919, 1.0249]])
    bias = np.array([0.6847, -0.7951])
    expected = np.array([0.4284, 0.5716])

    out = classification_head(sequence, weight, bias)
    assert np.allclose(out, expected, atol=1e-3)
