"""
pytest data/app_data/00-math-and-statistics/04-information-theory/03-kl-divergence/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"00-math-and-statistics/04-information-theory/{Path(__file__).resolve().parent.name}")
kl_divergence = _module.kl_divergence


def test_kl_divergence_of_p_with_itself_is_zero():
    p = np.array([0.5, 0.3, 0.2])
    assert np.isclose(kl_divergence(p, p), 0.0, atol=1e-10)


def test_kl_divergence_is_never_negative():
    rng = np.random.default_rng(0)
    for _ in range(10):
        p_raw = rng.uniform(size=5)
        p = p_raw / p_raw.sum()
        q_raw = rng.uniform(size=5)
        q = q_raw / q_raw.sum()
        assert kl_divergence(p, q) >= -1e-9


def test_kl_divergence_matches_hand_computation():
    p = np.array([1.0, 0.0])
    q = np.array([0.25, 0.75])
    # H(p,q) = 2.0 (from 02-cross-entropy's own hand-computed test),
    # H(p) = 0.0 (one-hot has zero entropy) -> KL = 2.0 - 0.0 = 2.0
    assert np.isclose(kl_divergence(p, q), 2.0)


def test_kl_divergence_is_asymmetric():
    p = np.array([0.9, 0.1])
    q = np.array([0.5, 0.5])
    forward = kl_divergence(p, q)
    backward = kl_divergence(q, p)
    assert not np.isclose(forward, backward)


def test_kl_divergence_increases_as_distributions_diverge_more():
    p = np.array([0.9, 0.1])
    close_q = np.array([0.85, 0.15])
    far_q = np.array([0.1, 0.9])
    assert kl_divergence(p, close_q) < kl_divergence(p, far_q)


def test_kl_divergence_subtracts_entropy_not_adds_it():
    # Directly targets a mutant that adds entropy instead of subtracting
    # it (cross_entropy(p, q) + entropy(p) instead of minus). For a
    # non-degenerate p, this produces a clearly larger, wrong result,
    # and breaks the "KL(p, p) == 0" property specifically.
    p = np.array([0.6, 0.4])
    result = kl_divergence(p, p)
    assert np.isclose(result, 0.0, atol=1e-9)
    assert not (result > 0.5)  # an additive mutant would give 2*entropy(p), clearly nonzero
