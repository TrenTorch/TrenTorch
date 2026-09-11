"""
pytest data/01-classical-ml/02-classification/09-production-bce-with-logits/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

bce_with_logits_loss = load_solution(f"01-classical-ml/02-classification/{Path(__file__).resolve().parent.name}").bce_with_logits_loss
sigmoid = load_solution("01-classical-ml/02-classification/01-sigmoid").sigmoid
bce_loss = load_solution("01-classical-ml/02-classification/02-bce-loss").bce_loss


def test_matches_naive_bce_on_ordinary_logits():
    rng = np.random.default_rng(12)
    z = rng.normal(size=50)
    y = rng.integers(0, 2, 50).astype(float)
    naive = bce_loss(sigmoid(z), y)
    fused = bce_with_logits_loss(z, y)
    assert np.isclose(naive, fused, atol=1e-6)


def test_stays_finite_where_naive_version_saturates():
    # z=100 already makes sigmoid(z) round to exactly 1.0 in float64 --
    # the naive path only survives because bce_loss clips p, silently
    # losing information. The fused version needs no clip at all.
    z = np.array([100.0, -100.0, 700.0, -700.0])
    y = np.array([1.0, 0.0, 1.0, 0.0])
    result = bce_with_logits_loss(z, y)
    assert np.isfinite(result)
    assert result < 1e-6  # all four predictions are correct and confident


def test_exponent_argument_never_exceeds_zero():
    # Structural check on the actual numerical-stability claim: patches
    # np.exp to assert every argument it's ever called with is <= 0,
    # which is only true if -np.abs(z) is really what's being exponentiated.
    calls = []
    original_exp = np.exp

    def spy_exp(x):
        calls.append(np.max(x) if np.size(x) else x)
        return original_exp(x)

    np.exp = spy_exp
    try:
        bce_with_logits_loss(np.array([500.0, -500.0]), np.array([1.0, 0.0]))
    finally:
        np.exp = original_exp
    assert all(c <= 0 for c in calls)


def test_matches_real_pytorch_bce_with_logits():
    # Ground truth from torch.nn.functional.binary_cross_entropy_with_logits,
    # generated once offline:
    #   z = torch.tensor([2.0, -3.0, 0.0, 800.0, -800.0])
    #   y = torch.tensor([1.0, 0.0, 1.0, 1.0, 0.0])
    #   F.binary_cross_entropy_with_logits(z, y, reduction='mean').item()
    # This test needs no torch installed to run -- the reference value
    # is baked in below (verified against a real torch run).
    z = np.array([2.0, -3.0, 0.0, 800.0, -800.0])
    y = np.array([1.0, 0.0, 1.0, 1.0, 0.0])
    EXPECTED = 0.17373250424861908
    assert np.isclose(bce_with_logits_loss(z, y), EXPECTED, atol=1e-4)
