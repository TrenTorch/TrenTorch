"""
pytest data/app_data/00-math-and-statistics/04-information-theory/01-entropy/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"00-math-and-statistics/04-information-theory/{Path(__file__).resolve().parent.name}")
entropy = _module.entropy


def test_entropy_of_fair_coin_is_one_bit():
    assert np.isclose(entropy(np.array([0.5, 0.5])), 1.0)


def test_entropy_of_certain_outcome_is_zero():
    assert np.isclose(entropy(np.array([1.0, 0.0])), 0.0)


def test_entropy_of_uniform_four_outcomes_is_two_bits():
    assert np.isclose(entropy(np.array([0.25, 0.25, 0.25, 0.25])), 2.0)


def test_entropy_does_not_crash_or_return_nan_on_zero_probability():
    result = entropy(np.array([1.0, 0.0, 0.0]))
    assert np.isfinite(result)
    assert np.isclose(result, 0.0)


def test_entropy_is_never_negative():
    rng = np.random.default_rng(0)
    for _ in range(10):
        raw = rng.uniform(size=5)
        probs = raw / raw.sum()
        assert entropy(probs) >= -1e-10


def test_entropy_with_natural_log_base_matches_bits_conversion():
    probs = np.array([0.5, 0.5])
    bits = entropy(probs, base=2.0)
    nats = entropy(probs, base=np.e)
    assert np.isclose(nats, bits * np.log(2.0))


def test_uniform_distribution_has_higher_entropy_than_skewed_one():
    uniform = np.array([0.25, 0.25, 0.25, 0.25])
    skewed = np.array([0.7, 0.1, 0.1, 0.1])
    assert entropy(uniform) > entropy(skewed)


def test_entropy_matches_known_oracle_value_for_a_biased_coin():
    # generated once, offline, via -sum(p*log2(p)) for p=[0.9, 0.1]
    probs = np.array([0.9, 0.1])
    expected = -(0.9 * np.log2(0.9) + 0.1 * np.log2(0.1))
    assert np.isclose(entropy(probs), expected, atol=1e-9)


def test_entropy_uses_correct_sign_not_a_missing_negation():
    # Directly targets a mutant that drops the leading negative sign:
    # entropy of a valid distribution should always be >= 0, but
    # sum(p*log(p)) itself (without negating) is always <= 0.
    probs = np.array([0.3, 0.7])
    unnegated = np.sum(probs * np.log2(np.clip(probs, 1e-12, 1.0)))
    result = entropy(probs)
    assert result > 0.0
    assert not np.isclose(result, unnegated)
    assert np.isclose(result, -unnegated)
