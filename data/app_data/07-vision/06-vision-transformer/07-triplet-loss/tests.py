"""
pytest data/app_data/07-vision/06-vision-transformer/07-triplet-loss/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

triplet_loss = load_solution(
    f"07-vision/06-vision-transformer/{Path(__file__).resolve().parent.name}"
).triplet_loss


# --- Basic correctness (the two the "Run" button samples) -----------------


def test_01_returns_a_nonnegative_float():
    rng = np.random.default_rng(0)
    anchor = rng.normal(size=(4, 3))
    positive = rng.normal(size=(4, 3))
    negative = rng.normal(size=(4, 3))
    loss = triplet_loss(anchor, positive, negative)
    assert isinstance(loss, float)
    assert loss >= 0.0


def test_02_positive_exactly_at_anchor_and_negative_far_away_gives_zero_loss():
    anchor = np.array([[0.0, 0.0]])
    positive = np.array([[0.0, 0.0]])  # distance 0
    negative = np.array([[100.0, 0.0]])  # distance 100, way more than margin
    loss = triplet_loss(anchor, positive, negative, margin=1.0)
    assert loss == 0.0


# --- Shape / general-case coverage -----------------------------------


def test_03_negative_exactly_at_anchor_gives_loss_equal_to_margin():
    # dist_to_positive = 0 (if positive also at anchor), dist_to_negative = 0
    # -> loss = max(0, 0 - 0 + margin) = margin
    anchor = np.array([[1.0, 2.0]])
    positive = np.array([[1.0, 2.0]])
    negative = np.array([[1.0, 2.0]])
    loss = triplet_loss(anchor, positive, negative, margin=0.5)
    assert np.isclose(loss, 0.5)


def test_04_averages_over_multiple_independent_triplets():
    anchor = np.array([[0.0, 0.0], [0.0, 0.0]])
    positive = np.array([[0.0, 0.0], [0.0, 0.0]])  # triplet 0: zero loss
    negative = np.array([[100.0, 0.0], [0.0, 0.0]])  # triplet 1: loss = margin
    loss = triplet_loss(anchor, positive, negative, margin=2.0)
    assert np.isclose(loss, (0.0 + 2.0) / 2)


# --- Parameter handling -------------------------------------------------


def test_05_larger_margin_never_decreases_the_loss():
    rng = np.random.default_rng(1)
    anchor = rng.normal(size=(5, 4))
    positive = rng.normal(size=(5, 4))
    negative = rng.normal(size=(5, 4))
    loss_small_margin = triplet_loss(anchor, positive, negative, margin=0.1)
    loss_large_margin = triplet_loss(anchor, positive, negative, margin=5.0)
    assert loss_large_margin >= loss_small_margin


# --- Edge cases ---------------------------------------------------------


def test_06_positive_farther_than_negative_produces_a_large_positive_loss():
    anchor = np.array([[0.0, 0.0]])
    positive = np.array([[10.0, 0.0]])  # far from anchor -- a BAD positive
    negative = np.array([[0.1, 0.0]])  # close to anchor -- a BAD negative
    loss = triplet_loss(anchor, positive, negative, margin=1.0)
    assert loss > 5.0


# --- Array hygiene ------------------------------------------------------


def test_07_does_not_mutate_its_inputs():
    rng = np.random.default_rng(2)
    anchor = rng.normal(size=(3, 4))
    positive = rng.normal(size=(3, 4))
    negative = rng.normal(size=(3, 4))
    a_copy, p_copy, n_copy = anchor.copy(), positive.copy(), negative.copy()
    triplet_loss(anchor, positive, negative)
    assert np.array_equal(anchor, a_copy)
    assert np.array_equal(positive, p_copy)
    assert np.array_equal(negative, n_copy)


# --- Independent correctness oracle -----------------------------------


def test_08_matches_real_pytorch_triplet_margin_loss_on_a_baked_reference_case():
    # Ground truth from the actual library, not our own derivation.
    # Generated once, offline, with:
    #   anchor, positive, negative = torch.randn(3, 4), torch.randn(3, 4), torch.randn(3, 4)
    #   loss = torch.nn.functional.triplet_margin_loss(
    #       anchor, positive, negative, margin=1.0, p=2, reduction='mean'
    #   )
    #
    # This test needs no torch installed to run -- the reference values
    # are baked in below.
    anchor = np.array(
        [
            [1.1982, -0.3998, -0.3476, -0.2759],
            [-2.3094, -1.0931, -0.0808, 0.7721],
            [-1.1370, -0.4773, -1.0679, 1.0688],
        ]
    )
    positive = np.array(
        [
            [1.3859, -0.6110, 0.8647, 0.8625],
            [-1.8944, -0.3187, 0.3835, 0.6440],
            [-0.6534, 0.8339, -1.5606, 0.4710],
        ]
    )
    negative = np.array(
        [
            [0.9000, 0.0511, -0.1384, -0.5572],
            [0.9167, -1.2498, 0.7457, 1.0732],
            [-1.7786, 0.9120, 1.8858, -0.5409],
        ]
    )
    expected_loss = 0.6808

    loss = triplet_loss(anchor, positive, negative, margin=1.0)
    assert abs(loss - expected_loss) < 1e-2
