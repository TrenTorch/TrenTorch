"""
pytest data/app_data/00-math-and-statistics/07-statistical-inference/05-statistical-significance-p-values/tests.py
"""

import sys
from pathlib import Path

import numpy as np
from scipy import stats

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(
    f"00-math-and-statistics/07-statistical-inference/{Path(__file__).resolve().parent.name}"
)
is_statistically_significant = _module.is_statistically_significant
expected_false_positives = _module.expected_false_positives
bonferroni_corrected_alpha = _module.bonferroni_corrected_alpha


def test_is_statistically_significant_below_threshold():
    assert is_statistically_significant(0.01, alpha=0.05)


def test_is_statistically_significant_above_threshold():
    assert not is_statistically_significant(0.2, alpha=0.05)


def test_is_statistically_significant_at_exact_boundary_is_false():
    # A p-value exactly equal to alpha is conventionally NOT significant
    # (strict <, not <=).
    assert not is_statistically_significant(0.05, alpha=0.05)


def test_expected_false_positives_matches_hand_computation():
    assert np.isclose(expected_false_positives(100, alpha=0.05), 5.0)


def test_expected_false_positives_scales_linearly_with_num_tests():
    assert np.isclose(expected_false_positives(200, alpha=0.05), 10.0)


def test_bonferroni_corrected_alpha_matches_hand_computation():
    assert np.isclose(bonferroni_corrected_alpha(20, alpha=0.05), 0.0025)


def test_bonferroni_correction_makes_significance_harder_to_reach():
    corrected = bonferroni_corrected_alpha(50, alpha=0.05)
    assert corrected < 0.05
    p_value = 0.01
    assert is_statistically_significant(p_value, alpha=0.05)
    assert not is_statistically_significant(p_value, alpha=corrected)


def test_multiple_testing_produces_false_positives_at_the_predicted_rate_empirically():
    # A direct empirical demonstration of the exact phenomenon this
    # question exists to name: run many independent tests where the
    # null hypothesis is ACTUALLY TRUE (both groups drawn from the
    # same distribution), and confirm the observed false-positive rate
    # roughly matches expected_false_positives' prediction.
    rng = np.random.default_rng(0)
    num_tests = 200
    alpha = 0.05
    false_positive_count = 0
    for _ in range(num_tests):
        a = rng.normal(0.0, 1.0, size=30)
        b = rng.normal(0.0, 1.0, size=30)  # same distribution: null is true
        _, p = stats.ttest_ind(a, b, equal_var=False)
        if is_statistically_significant(p, alpha):
            false_positive_count += 1

    predicted = expected_false_positives(num_tests, alpha)
    assert abs(false_positive_count - predicted) < predicted  # within a generous statistical margin


def test_bonferroni_correction_controls_the_empirical_false_positive_rate():
    # Same simulation, but using the Bonferroni-corrected threshold:
    # the false-positive count should now be dramatically lower.
    rng = np.random.default_rng(1)
    num_tests = 200
    alpha = 0.05
    corrected_alpha = bonferroni_corrected_alpha(num_tests, alpha)
    false_positive_count = 0
    for _ in range(num_tests):
        a = rng.normal(0.0, 1.0, size=30)
        b = rng.normal(0.0, 1.0, size=30)
        _, p = stats.ttest_ind(a, b, equal_var=False)
        if is_statistically_significant(p, corrected_alpha):
            false_positive_count += 1

    assert false_positive_count <= expected_false_positives(num_tests, alpha)


def test_bonferroni_corrected_alpha_divides_not_multiplies():
    # Directly targets a mutant that multiplies instead of dividing:
    # dividing must always shrink alpha as num_tests grows, multiplying
    # would grow it instead.
    small_correction = bonferroni_corrected_alpha(2, alpha=0.05)
    large_correction = bonferroni_corrected_alpha(100, alpha=0.05)
    assert large_correction < small_correction
    assert large_correction < 0.05
